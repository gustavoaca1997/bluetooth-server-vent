float RR = 0.0,   // Respiratory Rate (RR) (breaths per minute): between 8 – 40.
      TV = 0.0,   // Tidal Volume (TV) (air volume pushed into lung): between 200 – 800 mL based on patient weight.
      IE = 0.0;   // I/E Ratio (inspiratory/expiration time ratio): recommended to start around 1:2; best if adjustable between range of 1:1 – 1:4.

const char endCharacter = ':';

enum BlueState {
  OFF_BLUE_STATE,     //  0
  ON_BLUE_STATE,      //  1
  VOLUME_BLUE_STATE,  //  2
  BPM_BLUE_STATE,     //  3
  IE_BLUE_STATE       //  4
};

BlueState blueState = OFF_BLUE_STATE;

BlueState charToBlueState(char c) {
  switch (c)
  {
  case 'V':
    return VOLUME_BLUE_STATE;

  case 'R':
    return BPM_BLUE_STATE;

  case 'I':
    return IE_BLUE_STATE;
  
  case '0':
    return OFF_BLUE_STATE;
    
  default:
    return blueState;
  }
}

float readBluetoothValue(BlueState valueState, float* value, float (*read_fun)()) {
  while (Serial.available() > 0 && Serial.peek() == endCharacter) {
    Serial.read();
  }
  
  if (Serial.available() > 0) {
    if (blueState == OFF_BLUE_STATE) {
      blueState = ON_BLUE_STATE;
    }
    
    if (blueState == ON_BLUE_STATE) {
      blueState = charToBlueState(Serial.read());
      Serial.print("New state: ");
      Serial.println(blueState);
    }
  }

  if (Serial.available() > 0 && blueState == valueState) {
    *value = Serial.parseFloat();
    Serial.print('\t');
    Serial.println(*value);
    blueState = ON_BLUE_STATE;
    return *value;
  }

  if (blueState == OFF_BLUE_STATE) {
    return read_fun();
  }
  return *value;
}

float readVolume() {
  return -1;
}

float readBpm() {
  return -1;
}

float readIeRatio() {
  return -1;
}

float readBluetoothVolume() {
  return readBluetoothValue(VOLUME_BLUE_STATE, &TV, &readVolume);
}

float readBluetoothBPM() {
  return readBluetoothValue(BPM_BLUE_STATE, &RR, &readBpm);
}

float readBluetoothIE() {
  return readBluetoothValue(IE_BLUE_STATE, &IE, &readIeRatio);
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  while(!Serial);
}

int i = 0;

void loop() {
  readBluetoothVolume();
  readBluetoothBPM();
  readBluetoothIE();

  Serial.flush();
}

void logChange(char* msg, float val) {
  Serial.print(msg);
  Serial.println(val);
}

void logIEChange(char* msg, float i, float e) {
  Serial.print(msg);
  Serial.print(i);
  Serial.print(':');
  Serial.println(e);
}
