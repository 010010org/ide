int counter = 0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  Serial.println("test" + String(counter));
  counter++;
  delay(100);
}
