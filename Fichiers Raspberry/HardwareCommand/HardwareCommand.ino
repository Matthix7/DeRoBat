/*******************************************
 * Motor Shield 1-Channel DC Motor + Servo
 * by DeRoBat
 ******************************************/

#include <Servo.h>

Servo monServomoteur;


int Freq;
char msg[10];
int cnt=0;
int val;
int Angle;
int Speed;


void setup() {
  
  Serial.begin(115200);
  Serial.println(" En attente ");

  monServomoteur.attach(6);
  //Setup Channel A
  pinMode(12, OUTPUT); //Initiates direction of Motor Channel A pin
  pinMode(3, OUTPUT); //Initiates Speed Channel A pin
  pinMode(9, OUTPUT); //Initiates Brake Channel A pin

  digitalWrite(9, LOW); 
}


void loop() {
    
   while (Serial.available() > 0 ){
      msg[cnt] = Serial.read();
      cnt ++;
      
      if (cnt == 4) {
        val = atoi(msg);
        cnt = 0;
      }
                      
      if (val >= 1000 && val < 1255){
        Angle = val - 1000;
        monServomoteur.write(Angle);
      }
      
      if (val >= 2000 && val < 2255){
        digitalWrite(12, HIGH);   //Establishes forward direction of Channel A
        Speed = val - 2000;
        analogWrite(3, Speed);
      }

      if (val >= 3000 && val < 3255){
        digitalWrite(12, LOW);   //Establishes backward direction of Channel A
        Speed = val - 3000;
        analogWrite(3, Speed);
      }
   }
}   
