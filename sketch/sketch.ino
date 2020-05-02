float RR = 8.0,   // Respiratory Rate (RR) (breaths per minute): between 8 – 40.
      TV = 200.0, // Tidal Volume (TV) (air volume pushed into lung): between 200 – 800 mL based on patient weight.
      I = 1.0,    // I/E Ratio (inspiratory/expiration time ratio): recommended to start around 1:2; best if adjustable between range of 1:1 – 1:4.
      E = 2.0;

/*
 * 0: Expecting byte indicating field: 'R', 'T' and 'I' correspond
 *    to RR, TV and I/E, respectively. 
 * 'R': Expecting RR value.
 * 'T': Expecting TV value.
 * 'I': Expecting I/E values.
 */
char state = '\0';

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available() > 0) 
    {
      switch(state) {
        case '\0':
          state = Serial.read();
          break;
        case 'R':
          RR = Serial.parseFloat();
          logChange("Respiration Rate changed to ", RR);
          resetState();
          break;
        case 'T':
          TV = Serial.parseFloat();
          logChange("Tidal Volumen changed to ", TV);
          resetState();
          break;
        case 'I':
          I = Serial.parseFloat();
          state = 'E';
          break;
        case 'E':
          Serial.read(); // Delimiter
          E = Serial.parseFloat();
          logIEChange("I/E ratio changed to ", I, E);
          resetState();
          break;
        default:
          resetState();
          break;
      }
    }
}

void resetState() {
  state = '\0';
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
