//sketch per far ricevere i dati dal computer all'arduino per controllare i motori del rover

#include <SoftwareSerial.h>
#define rxPin 2
#define txPin 3
SoftwareSerial BL(rxPin, txPin); (definisco il nome del modulo bluetooth da richiamre nelle funzioni dello sketch)
#define baudrate 9600


void setup() {

  Serial.begin(baudrate);
  BL.begin(baudrate);

}

void loop() {

  if(BL.available()) {

    String input = BL.readStringUntil("/n");
    input.trim();
  }  


}


void avanti() {

  }


void indietro() {

  }


  void sinistra() {

  }


  void destra() {

  }
