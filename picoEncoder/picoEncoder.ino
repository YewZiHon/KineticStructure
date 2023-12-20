#include "ArduinoJson.h"

volatile int32_t position[24]={0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
volatile int8_t direction[24]={0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};

StaticJsonDocument<8192> doc;

//timer and counter
const uint32_t STARTTIME= 5000;//5s wait
const uint32_t TIMESTEP= 10 ;
uint32_t stepcounter = 0;


  void f0(){
    const int8_t encoder=0;
    if (direction[encoder]==1){
      position[encoder]+=1;
    }
    else if (direction[encoder]==-1){
      position[encoder]-=1;
    }
  }
  void f1(){
    const int8_t encoder=1;
    if (direction[encoder]==1){
      position[encoder]+=1;
    }
    else if (direction[encoder]==-1){
      position[encoder]-=1;
    }
  }
  void f2(){
    const int8_t encoder=2;
    if (direction[encoder]==1){
      position[encoder]+=1;
    }
    else if (direction[encoder]==-1){
      position[encoder]-=1;
    }
  }
  void f3(){
    const int8_t encoder=3;
    if (direction[encoder]==1){
      position[encoder]+=1;
    }
    else if (direction[encoder]==-1){
      position[encoder]-=1;
    }
  }
  void f4(){
    const int8_t encoder=4;
    if (direction[encoder]==1){
      position[encoder]+=1;
    }
    else if (direction[encoder]==-1){
      position[encoder]-=1;
    }
  }
  void f5(){
    const int8_t encoder=5;
    if (direction[encoder]==1){
      position[encoder]+=1;
    }
    else if (direction[encoder]==-1){
      position[encoder]-=1;
    }
  }
  void f6(){
    const int8_t encoder=6;
    if (direction[encoder]==1){
      position[encoder]+=1;
    }
    else if (direction[encoder]==-1){
      position[encoder]-=1;
    }
  }
  void f7(){
    const int8_t encoder=7;
    if (direction[encoder]==1){
      position[encoder]+=1;
    }
    else if (direction[encoder]==-1){
      position[encoder]-=1;
    }
  }
  void f8(){
    const int8_t encoder=8;
    if (direction[encoder]==1){
      position[encoder]+=1;
    }
    else if (direction[encoder]==-1){
      position[encoder]-=1;
    }
  }
  void f9(){
    const int8_t encoder=9;
    if (direction[encoder]==1){
      position[encoder]+=1;
    }
    else if (direction[encoder]==-1){
      position[encoder]-=1;
    }
  }
  void f10(){
    const int8_t encoder=10;
    if (direction[encoder]==1){
      position[encoder]+=1;
    }
    else if (direction[encoder]==-1){
      position[encoder]-=1;
    }
  }
  void f11(){
    const int8_t encoder=11;
    if (direction[encoder]==1){
      position[encoder]+=1;
    }
    else if (direction[encoder]==-1){
      position[encoder]-=1;
    }
  }
  void f12(){
    const int8_t encoder=12;
    if (direction[encoder]==1){
      position[encoder]+=1;
    }
    else if (direction[encoder]==-1){
      position[encoder]-=1;
    }
  }
  void f13(){
    const int8_t encoder=13;
    if (direction[encoder]==1){
      position[encoder]+=1;
    }
    else if (direction[encoder]==-1){
      position[encoder]-=1;
    }
  }
  void f14(){
    const int8_t encoder=14;
    if (direction[encoder]==1){
      position[encoder]+=1;
    }
    else if (direction[encoder]==-1){
      position[encoder]-=1;
    }
  }
  void f15(){
    const int8_t encoder=15;
    if (direction[encoder]==1){
      position[encoder]+=1;
    }
    else if (direction[encoder]==-1){
      position[encoder]-=1;
    }
  }
  void f16(){
    const int8_t encoder=16;
    if (direction[encoder]==1){
      position[encoder]+=1;
    }
    else if (direction[encoder]==-1){
      position[encoder]-=1;
    }
  }
  void f17(){
    const int8_t encoder=17;
    if (direction[encoder]==1){
      position[encoder]+=1;
    }
    else if (direction[encoder]==-1){
      position[encoder]-=1;
    }
  }
  void f18(){
    const int8_t encoder=18;
    if (direction[encoder]==1){
      position[encoder]+=1;
    }
    else if (direction[encoder]==-1){
      position[encoder]-=1;
    }
  }
  void f19(){
    const int8_t encoder=19;
    if (direction[encoder]==1){
      position[encoder]+=1;
    }
    else if (direction[encoder]==-1){
      position[encoder]-=1;
    }
  }
  void f20(){
    const int8_t encoder=20;
    if (direction[encoder]==1){
      position[encoder]+=1;
    }
    else if (direction[encoder]==-1){
      position[encoder]-=1;
    }
  }
  void f21(){
    const int8_t encoder=21;
    if (direction[encoder]==1){
      position[encoder]+=1;
    }
    else if (direction[encoder]==-1){
      position[encoder]-=1;
    }
  }
  void f22(){
    const int8_t encoder=22;
    if (direction[encoder]==1){
      position[encoder]+=1;
    }
    else if (direction[encoder]==-1){
      position[encoder]-=1;
    }
  }
  void f23(){
    const int8_t encoder=23;
    if (direction[encoder]==1){
      position[encoder]+=1;
    }
    else if (direction[encoder]==-1){
      position[encoder]-=1;
    }
  }

void setup() {

//setup pins
  for(uint8_t i =0; i<24;i++){
    pinMode(i,INPUT_PULLDOWN);
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
  attachInterrupt(12, f12, RISING);
  attachInterrupt(13, f13, RISING);
  attachInterrupt(14, f14, RISING);
  attachInterrupt(15, f15, RISING);
  attachInterrupt(16, f16, RISING);
  attachInterrupt(17, f17, RISING);
  attachInterrupt(18, f18, RISING);
  attachInterrupt(19, f19, RISING);
  attachInterrupt(20, f20, RISING);
  attachInterrupt(21, f21, RISING);
  attachInterrupt(22, f22, RISING);
  attachInterrupt(23, f23, RISING);
  direction[0]=1;


//other stuff
  Serial.println("initDone");

}

void loop() {

    
  


}
