#include "ArduinoJson.h"


volatile int32_t position[12]={0,0,0,0,0,0,0,0,0,0,0,0};

#define _1

#ifdef _0
const uint8_t clk[12]={0,1,2,3,4,5,6,7,8,9,10,11};
const uint8_t dat[12]={12,13,14,15,16,17,18,19,20,21,22,26};

#elif defined(_1)
const uint8_t clk[12]={0,2,4,6,8,10,12,14,16,18,20,22};
const uint8_t dat[12]={1,3,5,7,9,11,13,15,17,19,21,26};
#endif

StaticJsonDocument<8192> doc;

//timer and counter
const uint32_t STARTTIME= 5000;//5s wait
const uint32_t TIMESTEP= 10 ;
uint32_t stepcounter = 0;

//
  void f0(){
    const int8_t encoder=0;
    if (digitalRead(dat[encoder])){
      position[encoder]+=1;
    }
    else{
      position[encoder]-=1;
    }
  }
  void f1(){
    const int8_t encoder=1;
    if (digitalRead(dat[encoder])){
      position[encoder]+=1;
    }
    else{
      position[encoder]-=1;
    }
  }
  void f2(){
    const int8_t encoder=2;
    if (digitalRead(dat[encoder])){
      position[encoder]+=1;
    }
    else{
      position[encoder]-=1;
    }
  }
  void f3(){
    const int8_t encoder=3;
    if (digitalRead(dat[encoder])){
      position[encoder]+=1;
    }
    else{
      position[encoder]-=1;
    }
  }
  void f4(){
    const int8_t encoder=4;
    if (digitalRead(dat[encoder])){
      position[encoder]+=1;
    }
    else{
      position[encoder]-=1;
    }
  }
  void f5(){
    const int8_t encoder=5;
    if (digitalRead(dat[encoder])){
      position[encoder]+=1;
    }
    else{
      position[encoder]-=1;
    }
  }
  void f6(){
    const int8_t encoder=6;
    if (digitalRead(dat[encoder])){
      position[encoder]+=1;
    }
    else{
      position[encoder]-=1;
    }
  }
  void f7(){
    const int8_t encoder=7;
    if (digitalRead(dat[encoder])){
      position[encoder]+=1;
    }
    else{
      position[encoder]-=1;
    }
  }
  void f8(){
    const int8_t encoder=8;
    if (digitalRead(dat[encoder])){
      position[encoder]+=1;
    }
    else{
      position[encoder]-=1;
    }
  }
  void f9(){
    const int8_t encoder=9;
    if (digitalRead(dat[encoder])){
      position[encoder]+=1;
    }
    else{
      position[encoder]-=1;
    }
  }
  void f10(){
    const int8_t encoder=10;
    if (digitalRead(dat[encoder])){
      position[encoder]+=1;
    }
    else{
      position[encoder]-=1;
    }
  }
  void f11(){
    const int8_t encoder=11;
    if (digitalRead(dat[encoder])){
      position[encoder]+=1;
    }
    else{
      position[encoder]-=1;
    }
  }


void setup() {

//setup pins
  for(uint8_t i =0; i<12;i++){
    pinMode(clk[i],INPUT_PULLDOWN);
  }
  for(uint8_t i =0; i<12;i++){
    pinMode(dat[i],INPUT_PULLDOWN);
  }
// setup interrupts
  while(!Serial);
  attachInterrupt(clk[0], f0, RISING);
  attachInterrupt(clk[1], f1, RISING);
  attachInterrupt(clk[2], f2, RISING);
  attachInterrupt(clk[3], f3, RISING);
  attachInterrupt(clk[4], f4, RISING);
  attachInterrupt(clk[5], f5, RISING);
  attachInterrupt(clk[6], f6, RISING);
  attachInterrupt(clk[7], f7, RISING);
  attachInterrupt(clk[8], f8, RISING);
  attachInterrupt(clk[9], f9, RISING);
  attachInterrupt(clk[10], f10, RISING);
  attachInterrupt(clk[11], f11, RISING);


//other stuff
  //Serial.println("initDone");
  while(1){
    if (Serial.available()){
      deserializeJson(doc, Serial);
      if (doc.containsKey("i")){
        #ifdef _0
        deserializeJson(doc, "{\"i\":\"E0\"}");
        #elif defined(_1)
        deserializeJson(doc, "{\"i\":\"E1\"}");
        #endif
        serializeJson(doc, Serial);
        Serial.print('\n');
        break;
      }
    }
  }
}

void loop() {
  if (Serial.available()){
    deserializeJson(doc, Serial);
    if (doc.containsKey("i")){
        #ifdef _0
        deserializeJson(doc, "{\"i\":\"E0\"}");
        #elif defined(_1)
        deserializeJson(doc, "{\"i\":\"E1\"}");
        #endif
        serializeJson(doc, Serial);
        Serial.print('\n');
      }
    if (doc.containsKey("r")){
      for(uint8_t i =0; i<12;i++){
        position[i]=0;
      }
    }
  }
  doc.clear();
  doc.garbageCollect();
  doc["0"]=position[0];
  doc["1"]=position[1];
  doc["2"]=position[2];
  doc["3"]=position[3];
  doc["4"]=position[4];
  doc["5"]=position[5];
  doc["6"]=position[6];
  doc["7"]=position[7];
  doc["8"]=position[8];
  doc["9"]=position[9];
  doc["A"]=position[10];
  doc["B"]=position[11];
  serializeJson(doc, Serial);
  Serial.print('\n');
  delay(50);

  if (!Serial){
    rp2040.reboot();
  }

}
