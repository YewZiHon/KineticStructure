#include <ArduinoJson.h>

const uint8_t outputs[2][24]={
  {12,10,8,6,4,22,24,26,28,30,32,34 , A0,A2,58,A6,A8,A10,A12,A14,52,50,48,46},
  {11,9, 7,5,3,23,25,27,29,31,33,35 , A1,57,A5,A7,A9,A11,A13,A15,53,51,49,47}
};

#define MAXPWM 255

volatile int16_t power[24]={
  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
};

bool toggle=0;
uint16_t pwmPhaseCount=0;

StaticJsonDocument<128> doc;
char input[64];
uint8_t inputState=0;

void setup(){
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

void loop(){
  
  if (Serial.available()){
    char i=Serial.read();
    if(i=='{'){
      inputState=1;
      memset(input,0,30);
      strcpy(input,"{");

    }
    else if(inputState==1){
      strncat(input,&i,1);
      if(i=='}'){
        inputState=2;
        //Serial.println(input);
      }
    }
    if (inputState==2){
      deserializeJson(doc, input);
      inputState=0;

      if (doc.containsKey("i")){
        deserializeJson(doc, "{\"i\":\"M0\"}");
        serializeJson(doc, Serial);
        Serial.print('\n');
      }

      if (doc.containsKey("p")){//motor number and set power
        uint8_t motorNumber = doc["m"];
        power[motorNumber]=doc["p"];
        //power[motorNumber]-=255;
        if (power[motorNumber]!=0){
          if (power[motorNumber]>0){
            power[motorNumber]=uint16_t(MAXPWM)-power[motorNumber]+1;
          }
          else{
            power[motorNumber]=(uint16_t(MAXPWM)+power[motorNumber]+1)*-1;
          }
        }
        //Serial.println(power[motorNumber]);
      }
    }
  }
  //Serial ENd
  
  pwmPhaseCount++;
  if (pwmPhaseCount>=MAXPWM){
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
/*
{"m":0,"p":255}{"m":1,"p":255}{"m":2,"p":255}{"m":3,"p":255}{"m":4,"p":255}{"m":5,"p":255}{"m":6,"p":255}{"m":7,"p":255}{"m":8,"p":255}{"m":9,"p":255}{"m":10,"p":255}{"m":11,"p":255}{"m":12,"p":255}{"m":13,"p":255}{"m":14,"p":255}{"m":15,"p":255}{"m":16,"p":255}{"m":17,"p":255}{"m":18,"p":255}{"m":19,"p":255}{"m":20,"p":255}
{"m":0,"p":-255}{"m":1,"p":-255}{"m":2,"p":-255}{"m":3,"p":-255}{"m":4,"p":-255}{"m":5,"p":-255}{"m":6,"p":-255}{"m":7,"p":-255}{"m":8,"p":-255}{"m":9,"p":-255}{"m":10,"p":-255}{"m":11,"p":-255}{"m":12,"p":-255}
*/