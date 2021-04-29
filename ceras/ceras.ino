//Includes
//  Free RTOS
#include <Arduino_FreeRTOS.h>
#include <FreeRTOSConfig.h>
#include <croutine.h>
#include <event_groups.h>
#include <FreeRTOSConfig.h>
#include <FreeRTOSVariant.h>
#include <list.h>
#include <message_buffer.h>
#include <mpu_wrappers.h>
#include <portable.h>
#include <portmacro.h>
#include <projdefs.h>
#include <queue.h>
#include <semphr.h>
#include <stack_macros.h>
#include <stream_buffer.h>
#include <task.h>
#include <timers.h>

//Run Config
#define wcetLevel 0
//0 = Allow variable WCET
//1 = Force only encoder/pot code
//2 = Force only proximity code (full WCET)

//Includes
//  IMU, Wire, I2C
#include "Simple_MPU6050.h" //This code from ZHomeSlice - https://github.com/ZHomeSlice/Simple_MPU6050

//Oscilloscope Timing
const int scopeTrigger_OSC_TRIG_pin = 42;
bool scopeTriggerPinState = false;

//IMU Sensor Vars
//  I2C Address
#define MPU6050_ADDR 0x68
//  Sensor Class
Simple_MPU6050 mpu;
//  Protect against FIFO overflow within IMU DMP
ENABLE_MPU_OVERFLOW_PROTECTION();
//  Helper Macro to prevent Spamming the Serial Connection - This code from ZHomeSlice - https://github.com/ZHomeSlice/Simple_MPU6050 
#define spamtimer(t) for (static uint32_t SpamTimer; (uint32_t)(millis() - SpamTimer) >= (t); SpamTimer = millis())
//  Helper Macro to print floats - This code from ZHomeSlice - https://github.com/ZHomeSlice/Simple_MPU6050
#define printfloatx(Name,Variable,Spaces,Precision,EndTxt) print(Name); {char S[(Spaces + Precision + 3)];Serial.print(F(" ")); Serial.print(dtostrf((float)Variable,Spaces,Precision ,S));}Serial.print(EndTxt);

//Proximity Sensor Vars
//  Pins
const int proxTrig_TRIG_pin = 39;
const int proxEcho_ECHO_pin = 37;
//  Physics Definitions
const float speedOfSound_cmPerUs = .0343;
//  Pulse Measurement
int pulseWidth = 0;
//  Distance Values
int dist = 0, sumDist = 0, avgDist = 0;
//  Loop Sampling
int proxSampleCount = 0;

//Potentiometer Vars
//  Measurement Vars
int potValue = 0;

//Motor Vars
//  Rotation Motor PWM and H Bridge Directions
const int rotPwm_ENA_pin = 5;
const int rotFwd_IN1_pin = 6;
const int rotRev_IN2_pin = 7;
//  Extension Motor PWM and H Bridge Directions
const int extPwm_ENB_pin = 10;
const int extFwd_IN3_pin = 9;
const int extRev_IN4_pin = 8;
//  Throttle Terms
int motorGyroThrottle = 0;
int motorPotentiometerThrottle = 0;

//Define PID Variables
//  Setpoints
//      Gyro Setpoint Schedule (degrees)
const int S_gyro[2] = {120, 0};
const int S_gyroSize = 2;
//      potentiometer Setpoints (ticks)
const int S_potentiometer[2] = {550,820};
const int S_potentiometerSize = 2;
//      Indices
int S_gyroIndex = 0;
int S_potentiometerIndex = 0;
//  Measurement
float gyroYaw = 0;
//  Error
float gyroError = 0;
int potentiometerError = 0;
//  Gains
//      kP ~ 100% throttle at 180 deg error
float gyrokP = 0.62;
//      kP ~ 100% throttle at 40 ticks error
 float potentiometerkP = 0.20;
//  Outputs
float gyroPIDoutput = 0;
float potentiometerPIDoutput = 0;
//  In Range Flag
bool inRange = false;


//Switched Control Logic
//  Error Boundaries (degrees)
const int B[3] = {10,45,180};

//Switching Logic
long t, tEnteredRange;

//Create two tasks
void vArmControlTask( void *pvParameters );

//Serial Setup
void serialSetup(){
    //Create serial connection
    Serial.begin(115200);

    //Wait for serial to be setup
    while (!Serial);
}

//Create clock
void clockSetup(){
    t = millis();
    tEnteredRange = t;
}

//Configure arm base motor
void rotationMotorSetup(){
    //Pin Config
    pinMode(rotPwm_ENA_pin,OUTPUT);
    pinMode(rotFwd_IN1_pin,OUTPUT);
    pinMode(rotRev_IN2_pin,OUTPUT);

    //Turn Motor Off
    //  Kill H Bridge
    digitalWrite(rotFwd_IN1_pin,0);
    digitalWrite(rotRev_IN2_pin,0);
    //  PWM Duty Cycle to 0%
    analogWrite(rotPwm_ENA_pin,pctToThrottle(0));
}

//Configure wrist motor
void extensionMotorSetup(){
    //Pin Config
    pinMode(extPwm_ENB_pin,OUTPUT);
    pinMode(extFwd_IN3_pin,OUTPUT);
    pinMode(extRev_IN4_pin,OUTPUT);

    //Turn Motor Off
    //  Kill H Bridge
    digitalWrite(extFwd_IN3_pin,0);
    digitalWrite(extRev_IN4_pin,0);
    //  PWM Duty Cycle to 0%
    analogWrite(extPwm_ENB_pin,pctToThrottle(0));

}

//Configure proximity sensor (ultrasonic rangefinder)
void proximitySetup(){
    //Pin Config
    pinMode(proxTrig_TRIG_pin,OUTPUT);
    pinMode(proxEcho_ECHO_pin,INPUT);
}

// Return PWM throttle (duty cycle) based on input percentage
int pctToThrottle(int pct){

    if(pct < 0){
        pct *= -1;
    }

    if(pct > 100){
        pct = 100;
    }

    return map(pct,0,100,0,255);
}

//Measure Rotation with potentiometer
void potentiometerMeasure(){

    //Get output A value
    potValue = analogRead(A15);
}

//Service Proximity Sensor
void proximityLoop(){

    //Clear Sum Values
    sumDist = 0;

    //Sum 
    for(proxSampleCount = 0; proxSampleCount < 3; proxSampleCount++){

        //Sample proximity sensor
        proximityMeasure();

        //Sum distance
        sumDist += dist;
    }

    //Compute Avg Prox Sensor Value
    avgDist = sumDist / proxSampleCount;
}

//Measure Distance with Proximity Sensor
void proximityMeasure(){

    //Trigger Ping
    digitalWrite(proxTrig_TRIG_pin,HIGH);

    //Delay for 10us to deliver signal (per HC-SR04 Datasheet pg. 4)
    // unsigned long tProxStart = micros();
    // while(micros() < tProxStart + 10)
    delayMicroseconds(10);

    //Halt trigger
    digitalWrite(proxTrig_TRIG_pin,LOW);

    //Measure the length of the return pulse - starts when LOW->HIGH, stops when HIGH->LOW
    //  Disable interrupts so pulse is not obstructed
    noInterrupts();
    //  Get pulse width from ECHO pin going HIGH for up to 9000us (time needed to sense a distance of 300cm or less)
    pulseWidth = pulseIn(proxEcho_ECHO_pin,HIGH,9000);
    //  Re-enable interrupts
    interrupts();

    //Calculate distance from Sound
    dist = ((pulseWidth * 171)/5000);
}

//Provide Error and Yaw values from controller and IMU DMP
int printWithDelay(int32_t *quat, uint16_t printDelay = 100) {

  //Print with delay using ZHomeslice Macro (This code from ZHomeSlice - https://github.com/ZHomeSlice/Simple_MPU6050)
  spamtimer(printDelay) {
    Serial.printfloatx(F("Error"),gyroError,9,4,F(", "));
    Serial.printfloatx(F("Yaw"),gyroYaw,9,4,F("\n"));
  }
}

//Value printing function
void printImuVals (int16_t *gyro, int16_t *accel, int32_t *quat, uint32_t *timestamp) {

  //Pick Serial.print delay value to prevent overloading
  uint8_t printDelay = 100;

  //Print quaternions with delay
  printWithDelay(quat, printDelay);
}

//Configure IMU
void imuSetup(){

    //Start I2C
    Wire.begin();

    //Set I2C clock to 400kHz
    Wire.setClock(400000);

    //Calibration
    mpu.SetAddress(MPU6050_ADDR).CalibrateMPU().load_DMP_Image();

    // mpu.on_FIFO(printImuVals);
}

//IMU Routine
void imuLoop(){

    //Handle FIFO queue in IMU DMP
    mpu.dmp_read_fifo();
}

//Perform measurement
void imuMeasure(){

    //Create Quaternion to map orientation
    Quaternion q;

    //Instantiate Gravity
    VectorFloat gravity;

    //Setup Yaw, Pitch, Roll
    float ypr[3] = { 0, 0, 0 };

    //Setup Degree Conversions
    float xyz[3] = { 0, 0, 0 };

    //Get Quaternion Representation
    mpu.GetQuaternion(&q, mpu.quat);

    //Get Gravity
    mpu.GetGravity(&gravity, &q);

    //Generate Yaw, Pitch, Roll from Quaternion and Gravity
    mpu.GetYawPitchRoll(ypr, &q, &gravity);

    //Convert to human readable format
    mpu.ConvertToDegrees(ypr, xyz);

    //Log Yaw
    gyroYaw = xyz[0];
}

//Set motor speed
void motorSetSpeed(int motorEnablePin, int motorFwdPin, int motorRevPin, int speed){

    //Soft Limit Check
    if(gyroYaw > B[2] || gyroYaw < -B[2])
        speed = 0;

    //Deadband
    if(abs(speed) < 2){
        speed = 0;
    }

    //Set H Bridge Fwd if speed is positive, Rev if negative
    digitalWrite(motorFwdPin,speed > 0);
    digitalWrite(motorRevPin,speed < 0);

    //Write to PWM
    analogWrite(motorEnablePin,pctToThrottle(speed));

}

//Setpoint Updates
void updateSetpoints(){

    inRange = false;

    //Increment setpoint, then mod by range
    S_gyroIndex++;
    S_gyroIndex = S_gyroIndex % S_gyroSize;
    S_potentiometerIndex++;
    S_potentiometerIndex = S_potentiometerIndex % S_potentiometerSize;
}

//Initialization
void setup() {

    //Create arm control task
    xTaskCreate(
        vArmControlTask,            //Task
        (const portCHAR *)"armCtrl",//Name
        256,                        // Stack size
        NULL,                       //Params to receive
        4,                          // priority
        NULL
        );                     //Handle
}

//Loop
void loop()
{
  // Looping is handled in tasks
}

//Arm Control Sensing and Computation Jobs
void vArmControlSensingComputationLoop(){
    
    //Service IMU (Gyro)
    imuLoop();

    //Measure Angular Position
    imuMeasure();

    //Calculate Error
    gyroError = S_gyro[S_gyroIndex] - gyroYaw;

    //Calculate Gyro PID Outout
    gyroPIDoutput = gyroError * gyrokP;

    //Determine whether to enable second (arm) stage:
    if(abs(gyroError) < B[1] || wcetLevel>0){

        //Service potentiometer
        potentiometerMeasure();

        //Calculate Error
        potentiometerError =  S_potentiometer[S_potentiometerIndex] - potValue;

        //Calculate potentiometer PID Output
        potentiometerPIDoutput = potentiometerError * potentiometerkP;

    }
}

//Actuation loop (motor commands)
void vArmControlActuationLoop(){

    //Indicate Boundary
    Serial.print("B2");

    //Set Rotation Motor speed to Gyro PID Outputs
    motorSetSpeed(rotPwm_ENA_pin,rotFwd_IN1_pin,rotRev_IN2_pin,(int)gyroPIDoutput);

    //Determine whether to enable second (arm) stage:
    if(abs(gyroError) < B[1] || wcetLevel>0){

        //Indicate Boundary
        Serial.print("1");

        //Set Extension Motor speed to potentiometer PID output
        motorSetSpeed(extPwm_ENB_pin,extFwd_IN3_pin,extRev_IN4_pin,(int)potentiometerPIDoutput);

        //Determine whether to enable third stage (proximity sensor end-effector) 
        if(abs(gyroError) < B[0] || wcetLevel>1){

            //Indicate Boundary
            Serial.print("0");

            //Service Proximity Sensor
            proximityMeasure();

        }
    }

    //Return on boundary indication 
    Serial.println(" ");

}

// Arm Control
void vArmControlTask( void * pvParameters){

    //Serial Setup
    serialSetup();

    //Clock Setup
    clockSetup();

    //Setup Devices
    //  Motors
    rotationMotorSetup();
    extensionMotorSetup();
    //  Sensors
    proximitySetup();
    imuSetup();

    //
    TickType_t xLastWakeTime;
    const TickType_t xFrequency = 1;

    //Setup reset times
    const int A[2] = {60,90};
    int ticksPassed = 0;

    //Establish bool for toggling pin
    bool runningState = false;

    //Establish toggle for indicating when control loop is running
    const int running_SIG_pin = 52;

    //Set Pin 12 as output.
    pinMode(scopeTrigger_OSC_TRIG_pin, OUTPUT);

    for( ;; )
    {

        //Perform Switched Control Task
        vArmControlSensingComputationLoop();

        //Update Setpoint if Necessary
        if(ticksPassed >= A[S_gyroIndex]){
            updateSetpoints();
            ticksPassed = 0;
        }

        //Indicate control loop has stopped executing
        runningState = !runningState;
        digitalWrite(running_SIG_pin,runningState);

        //Delay until next period
        vTaskDelayUntil(&xLastWakeTime,xFrequency);
        xLastWakeTime = xTaskGetTickCount();
        ticksPassed+=1;

        //Indicate new job release
        digitalWrite(scopeTrigger_OSC_TRIG_pin,scopeTriggerPinState);

        //Toggle scope pin as indication processor is still alive
        scopeTriggerPinState = !scopeTriggerPinState;

        //Indicate control loop is being executed
        runningState = !runningState;
        digitalWrite(running_SIG_pin,runningState);

        //Perform Actuation
        vArmControlActuationLoop();

    }
}