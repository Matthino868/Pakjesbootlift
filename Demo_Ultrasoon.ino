#define trigPinSide 10
#define echoPinSide 11
#define trigPinFront 12
#define echoPinFront 13
#define LedCloseSide 9
#define LedGoodSide 8
#define LedFarSide 7
#define LedCloseFront 6
#define LedGoodFront 5
#define LedFarFront 4


void setup() {
  Serial.begin (9600);
  pinMode(trigPinSide, OUTPUT);
  pinMode(echoPinSide, INPUT);
  pinMode(trigPinFront, OUTPUT);
  pinMode(echoPinFront, INPUT);
  pinMode(LedCloseSide, OUTPUT);
  pinMode(LedGoodSide, OUTPUT);
  pinMode(LedFarSide, OUTPUT);
  pinMode(LedCloseFront, OUTPUT);
  pinMode(LedGoodFront, OUTPUT);
  pinMode(LedFarFront, OUTPUT);
}

void loop() {
  int durationSide, distanceSide;
  int durationFront, distanceFront;
  digitalWrite(trigPinSide, HIGH);
  delayMicroseconds(1000);
  digitalWrite(trigPinSide, LOW);
  durationSide = pulseIn(echoPinSide, HIGH);
  distanceSide = (durationSide/2) / 29.1;
   if (distanceSide > 15){
    digitalWrite(LedFarSide, HIGH);
    digitalWrite(LedGoodSide, LOW);
    digitalWrite(LedCloseSide, LOW);
  }


    if (distanceSide >= 10 && distanceSide <= 15){
    
    digitalWrite(LedFarSide, LOW);
    digitalWrite(LedGoodSide, HIGH);
    digitalWrite(LedCloseSide, LOW);
  }
    if (distanceSide < 10){
    
    digitalWrite(LedFarSide, LOW);
    digitalWrite(LedGoodSide, LOW);
    digitalWrite(LedCloseSide, HIGH);
  }

    Serial.println("Side");
    Serial.print(distanceSide);
    Serial.println(" cm");
  

  delay(50);
  
  digitalWrite(trigPinFront, HIGH);
  delayMicroseconds(1000);
  digitalWrite(trigPinFront, LOW);
  durationFront = pulseIn(echoPinFront, HIGH);
  distanceFront = (durationFront/2) / 29.1;
    if (distanceFront > 10){
    
    digitalWrite(LedFarFront, HIGH);
    digitalWrite(LedGoodFront, LOW);
    digitalWrite(LedCloseFront, LOW);
  }
    if (distanceFront >= 5 && distanceFront <= 10){
    
    digitalWrite(LedFarFront, LOW);
    digitalWrite(LedGoodFront, HIGH);
    digitalWrite(LedCloseFront, LOW);
  }
    if (distanceFront < 5){
    
    digitalWrite(LedFarFront, LOW);
    digitalWrite(LedGoodFront, LOW);
    digitalWrite(LedCloseFront, HIGH);
  }
  

  
  delay(50);
}
