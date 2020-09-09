int counter = 0;

void setup() {
  Serial.begin(9600);
  pinMode(4, OUTPUT);
  digitalWrite(4, HIGH);
  delay(1000);
  digitalWrite(4, LOW);
}

void loop() {
  /*Serial.println("test" + String(counter));
  counter++;
  delay(100);*/
}
