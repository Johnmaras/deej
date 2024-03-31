const int NUM_SLIDERS = 1;
const int analogInputs[NUM_SLIDERS] = { A2 };
const int buttonPin = 2;  // the number of the pushbutton pin
const String PAIR_TOKEN = "ThisIsDeej";

int analogSliderValues[NUM_SLIDERS];
int buttonState = 0;  // variable for reading the pushbutton status
bool devicePaired = false;

void setup() {
  for (int i = 0; i < NUM_SLIDERS; i++) {
    pinMode(analogInputs[i], INPUT);
  }

  // initialize the pushbutton pin as an input:
  pinMode(buttonPin, INPUT);

  Serial.begin(9600);
}

void loop() {
  // pairDevice(false);
  handleButton();
  updateSliderValues();
  sendSliderValues();  // Actually send data (all the time)
  // printSliderValues(); // For debug
  delay(10);
}

void pairDevice(bool force) {
  if (!devicePaired || force) {
    for (int i = 0; i < 1000; i++) {
      Serial.println(PAIR_TOKEN);
      delay(10);
    }
    devicePaired = true;
  }
}

void handleButton() {
  // read the state of the pushbutton value:
  buttonState = digitalRead(buttonPin);
  // check if the pushbutton is pressed. If it is, the buttonState is HIGH:
  if (buttonState == HIGH) {
    pairDevice(true);
    // Serial.println("Hi");
  }
}
void updateSliderValues() {
  for (int i = 0; i < NUM_SLIDERS; i++) {
    analogSliderValues[i] = analogRead(analogInputs[i]);
  }
}

void sendSliderValues() {
  String builtString = String("");

  for (int i = 0; i < NUM_SLIDERS; i++) {
    builtString += String((int)analogSliderValues[i]);

    if (i < NUM_SLIDERS - 1) {
      builtString += String("|");
    }
  }

  Serial.println(builtString);
}

void printSliderValues() {
  for (int i = 0; i < NUM_SLIDERS; i++) {
    String printedString = String("Slider #") + String(i + 1) + String(": ") + String(analogSliderValues[i]) + String(" mV");
    Serial.write(printedString.c_str());

    if (i < NUM_SLIDERS - 1) {
      Serial.write(" | ");
    } else {
      Serial.write("\n");
    }
  }
}