#include <ArduinoJson.h>

const uint8_t outputs[2][24]={
  {2,3,4,5,6,7,8,9,10,11,12,12,22,23,24,25,26,27,28,29,30,31,32,33},
  {34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,A0,A1,A2}
};

#define MAXPWM 255

volatile int16_t power[24]={
  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
};

bool toggle=0;
uint16_t pwmPhaseCount=0;

StaticJsonDocument<256> doc;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  for(uint8_t i=0; i<2;i++){
    for(uint8_t j=0; j<24;j++){
      pinMode(outputs[i][j],OUTPUT);
      digitalWrite(outputs[i][j],1);
    }
  }

  pinMode(13,OUTPUT);
}

void loop() {
  if (Serial.available()){
    deserializeJson(doc, Serial);
    serializeJson(doc, Serial);
    if (doc.containsKey("m") && doc.containsKey("p")){//motor number and set power
      uint8_t motorNumber = doc["m"];
      power[motorNumber]=doc["p"];
      Serial.print(motorNumber);
      Serial.print(" ");
      Serial.println(power[motorNumber]);
    }
  }
  //Serial.println(pwmPhaseCount);
  pwmPhaseCount++;
  if (pwmPhaseCount>=255){
    pwmPhaseCount=0;
    digitalWrite(13,toggle);
    toggle = !toggle;
    for(uint8_t i=0; i<2;i++){
      for(uint8_t j=0; j<24;j++){
        digitalWrite(outputs[i][j],0);
      }
    }
  }
  for(uint8_t j=0; j<24;j++){
    if (power[j]!=0){
      if (power[j]<0 && (power[j]*-1)==pwmPhaseCount){
        digitalWrite(outputs[0][j],1);
      }
      if (power[j]>0 && power[j]==pwmPhaseCount){
        digitalWrite(outputs[1][j],1);
      }
    }
  }
}
