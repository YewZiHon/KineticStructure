#include "ArduinoJson.h"

volatile int32_t position[12]={0,0,0,0,0,0,0,0,0,0,0,0};
const uint8_t clk[12]={0,1,2,3,4,5,6,7,8,9,10,11};
const uint8_t dat[12]={12,13,14,15,16,17,18,19,20,21,22,26};

StaticJsonDocument<8192> doc;

//timer and counter
const uint32_t STARTTIME= 5000;//5s wait
const uint32_t TIMESTEP= 10 ;
uint32_t stepcounter = 0;


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
  attachInterrupt(0, f0, RISING);
  attachInterrupt(1, f1, RISING);
  attachInterrupt(2, f2, RISING);
  attachInterrupt(3, f3, RISING);
  attachInterrupt(4, f4, RISING);
  attachInterrupt(5, f5, RISING);
  attachInterrupt(6, f6, RISING);
  attachInterrupt(7, f7, RISING);
  attachInterrupt(8, f8, RISING);
  attachInterrupt(9, f9, RISING);
  attachInterrupt(10, f10, RISING);
  attachInterrupt(11, f11, RISING);


//other stuff
  //Serial.println("initDone");
  while(1){
    break;
    if (Serial.available()){
      deserializeJson(doc, Serial);
      if (doc.containsKey("i")){
        deserializeJson(doc, "{\"i\":\"E0\"}");
        serializeJson(doc, Serial);
        break;
      }
    }
  }
}

void loop() {
  if (Serial.available()){
    deserializeJson(doc, Serial);
    if (doc.containsKey("i")){
        deserializeJson(doc, "{\"i\":\"E0\"}");
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
  


}
