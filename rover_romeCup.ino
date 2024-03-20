//CUNDUCTUM ROVER
//IIS EDOARDO AMALDI
//ROMECUP 2024, UNIVERSITA' DEGLI STUDI DI ROMA "TOR VERGATA"

//VELOCITA' MOTORI ROTAZIONE 1700
//TEMPO ROTAZIONE 90 1700
//VELOCITA' CROCIERA MOTORI 70
//ADDR:98D3:41:F6F4EA
//CLASS:1f00

#include <SoftwareSerial.h>
#define rxPin 4
#define txPin 3
SoftwareSerial BL(rxPin, txPin); // (definisco il nome del modulo bluetooth da richiamre nelle funzioni dello sketch)
#define baudrate 9600

#define trigPin 11
#define echoPin 12
long durata, cm;
int x, y, tempo_sterzo;
float a;

//pin del modulo di gestione dei motori
int motor1pin1 = 9;
int motor1pin2 = 8;

int motor2pin1 = 7;
int motor2pin2 = 6;
int ena = 10;
int enb = 5;




void setup() {

  Serial.begin(baudrate);
  BL.begin(baudrate);
  
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  pinMode(motor1pin1, OUTPUT);
  pinMode(motor1pin2, OUTPUT);
  pinMode(motor2pin1, OUTPUT);
  pinMode(motor2pin2, OUTPUT);

  //pin velocità motori
  pinMode(ena,   OUTPUT); 
  pinMode(enb, OUTPUT);
   
}

void loop() {
/*
  int x = 0;
  int y = 0;
  float a = 0.0;
  int tempo_sterzo = 0;
*/

    
    
    /*al.println(input);
    int x = 0;
    int y = 0;
    float a = 0.00;
    int index1 = input.indexOf(',');
    int index2 = input.indexOf(',' , index1 + 1);
    if (index1 != -1 && index2 != -1) {
      String x_str = input.substring(0, index1);
      String y_str = input.substring(index1 + 1, index2);
      String a_str = input.substring(index2 + 1);
      x = x_str.toInt();
      y = y_str.toInt();
      a = a_str.toFloat();
      //Serial.println(x);

      
  } */ 
 
 
 
  distanza();
  lettura();
  while(cm >= 10 && BL.available()) {
    distanza();
    Serial.print(" cm: ");
    Serial.println(cm);
    lettura();



    while(y >= 230 && BL.available()) {

      lettura();
      distanza();
      Serial.print("y: ");
      Serial.print(y);
      avanti();

      if (cm <= 10 && cm != 0) {
        fermo();
        }
      if (x <= 200 && x != 0 && a != 0) {
          //gira angolo verso destra
          fermo();
          int tempo_sterzo = map(a, 0, 3, 0, 1700);
          destra();
          delay(tempo_sterzo);
          fermo();
        }
      else if (x >= 550 && a != 0) {
          //gira angolo verso sinistra
          fermo();
          int tempo_sterzo = map(a, 0, 3, 0, 1700);
          sinistra();
          delay(tempo_sterzo);
          fermo();

       } 
       if (!BL.available() || y < 230) {
        break;
        } 
      
    } 
    fermo();
    distanza();
    if (!BL.available() || cm < 10) {
        break;
        } 
    
  }  

  /*if(BL.available()) {

    String input = BL.readStringUntil("/n");
    input.trim();
  } */
 fermo();

}

void lettura() { 
  //if (BL.available() > 0) {
  String input = String(BL.readStringUntil('.'));
  
    //Serial.println(input);
    /*
    int x = 0;
    int y = 0;
    float a = 0.00;
    */
    int index1 = input.indexOf(',');
    int index2 = input.indexOf(',' , index1 + 1);
    if (index1 != -1 && index2 != -1) {
      String x_str = input.substring(0, index1);
      String y_str = input.substring(index1 + 1, index2);
      String a_str = input.substring(index2 + 1);
      x = x_str.toInt();
      y = y_str.toInt();
      a = a_str.toFloat();
      //Serial.println(x);
      return;
      }
    //}
    return;
  }

void avanti() {
  analogWrite(ena, 70); //ENA   pin
  analogWrite(enb, 70); //ENB pin
  digitalWrite(motor1pin1,   HIGH);
  digitalWrite(motor1pin2, LOW);
  digitalWrite(motor2pin1, HIGH);
  digitalWrite(motor2pin2, LOW);

  }


void fermo() {
  digitalWrite(motor1pin1,   HIGH);
  digitalWrite(motor1pin2, HIGH);
  digitalWrite(motor2pin1,   HIGH);
  digitalWrite(motor2pin2, HIGH);

  }


  void sinistra() {

  analogWrite(ena, 120); //ENA   pin
  analogWrite(enb, 120); //ENB pin
  digitalWrite(motor2pin1,   HIGH);
  digitalWrite(motor2pin2, LOW);
  }


  void destra() {

  analogWrite(ena, 100); //ENA   pin
  analogWrite(enb, 100); //ENB pin
  digitalWrite(motor1pin1,   HIGH);
  digitalWrite(motor1pin2, LOW);
  }

  void distanza() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  durata = pulseIn(echoPin, HIGH);
  cm = durata / 58;
  
  return;
  }
