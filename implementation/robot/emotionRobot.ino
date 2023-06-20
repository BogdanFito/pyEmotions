#include "Trackcv.h"
#include "String.h"
#include <Display.h>
#include <Servo.h>


Display display(UART1);

int prev_emotion = 0;
int color = YELLOW;
int new_color = YELLOW;
Servo servo_port_OUT2;
Servo servo_port_OUT3;
int _ABVAR_1_a;

void setup() {
  Serial.begin(115200);
  Serial2.begin(115200);
  display.brightness(500);
  servo_port_OUT2.attach(OUT2, SMALL_SERVO);
  servo_port_OUT3.attach(OUT3, SMALL_SERVO);
  Serial.print("start trackcv...\n");
  Trackcv_init(comm_recv, comm_send, 0);
  servo_port_OUT2.write( 0 );
  servo_port_OUT3.write( 180 );
}

void clear_emotion() {
  //clear smile
  display.line(120, 70, 140, 67, BLACK);
  display.line(190, 67, 210, 70, BLACK);
  display.line(160, 160, 120, 140, BLACK);
  display.line(160, 160, 200, 140, BLACK);

  //clear sad
  display.line(130, 70, 150, 70, BLACK);
  display.line(190, 70, 210, 70, BLACK);
  display.line(120, 160, 160, 140, BLACK);
  display.line(160, 140, 200, 160, BLACK);

  //clear no_emotion
  display.line(120, 160, 200, 160, BLACK);

  //clear anger
  display.line(120, 65, 140, 70, BLACK);
  display.line(190, 70, 210, 65, BLACK);
  display.line(140, 160, 180, 160, BLACK);


  //clear suprise
  display.line(130, 60, 150, 60, BLACK);
  display.line(180, 60, 200, 60, BLACK);
  display.circle(160, 150, 10, BLACK);
}

void smile() {

    delay(250);
//  display.clear();

  if (prev_emotion != 1 || new_color != color) {

      clear_emotion();
      color = new_color;
      display.circle(160, 120, 100, color);

      display.line(120, 70, 140, 67, color);
      display.circleFilled(130, 100, 10, color);

      display.line(190, 67, 210, 70, color);
      display.circleFilled(190, 100, 10, color);

      display.line(160, 160, 120, 140, color);
      display.line(160, 160, 200, 140, color);
      servo_port_OUT2.write( 180 );
      servo_port_OUT3.write( 0 );
      prev_emotion = 1;
  } else {
  }
}

void sad() {

  delay(250);
//  display.clear();

  if (prev_emotion != 2 || new_color != color) {

      clear_emotion();
      color = new_color;
      display.circle(160, 120, 100, color);

      display.line(130, 70, 150, 70, color);
      display.circleFilled(130, 100, 10, color);

      display.line(190, 70, 210, 70, color);
      display.circleFilled(190, 100, 10, color);

      display.line(120, 160, 160, 140, color);
      display.line(160, 140, 200, 160, color);
      servo_port_OUT2.write( 0 );
      servo_port_OUT3.write( 180 );
      prev_emotion = 2;
  } else {
  }
}

void anger() {

  delay(250);
//  display.clear();
  if (prev_emotion != 3 || new_color != color) {

      clear_emotion();
      color = new_color;
      display.circle(160, 120, 100, color);

      display.line(120, 65, 140, 70, color);
      display.circleFilled(130, 100, 10, color);

      display.line(190, 70, 210, 65, color);
      display.circleFilled(190, 100, 10, color);

      display.line(140, 160, 180, 160, color);

  for (_ABVAR_1_a=1; _ABVAR_1_a<= ( 3 ); ++_ABVAR_1_a )
  {
    servo_port_OUT2.write( 0 );
    servo_port_OUT3.write( 0 );
    delay( 300 );
    servo_port_OUT2.write( 180 );
    servo_port_OUT3.write( 180 );
    delay( 300 );
  }
      prev_emotion = 3;
  } else {
  }
}

void suprise() {

  delay(250);
//  display.clear();
  if (prev_emotion != 4 || new_color != color) {

      clear_emotion();
      color = new_color;
      display.circle(160, 120, 100, color);

      display.line(130, 60, 150, 60, color);
      display.circleFilled(130, 100, 10, color);

      display.line(180, 60, 200, 60, color);
      display.circleFilled(190, 100, 10, color);

      display.circle(160, 150, 10, color);
 for (_ABVAR_1_a=1; _ABVAR_1_a<= ( 5 ); ++_ABVAR_1_a )
  {
    servo_port_OUT2.write( 90 );
    servo_port_OUT3.write( 90 );
    delay( 200 );
    servo_port_OUT2.write( 180 );
    servo_port_OUT3.write( 0 );
    delay( 200 );
  }
      prev_emotion = 4;
  } else {
  }
}

void no_emotion() {

    delay(250);
//  display.clear();
  if (prev_emotion != 0 || new_color != color) {

      clear_emotion();
      color = new_color;
      display.circle(160, 120, 100, color);
      display.circleFilled(130, 100, 10, color);
      display.circleFilled(190, 100, 10, color);
    //  display.line(160, 160, 120, 140, BLUE);
      display.line(120, 160, 200, 160, color);
      servo_port_OUT2.write( 90 );
      servo_port_OUT3.write( 90 );
      prev_emotion = 0;
  } else {

  }
}

bool inited = false;

void loop() {
  if(!inited) {
    if (trackcv_get_errno() != ERR_OK) {
      Serial.println("trackcv...fail");
      builtInRGB(RED);
      if(trackcv_check()) {
        Serial.print("check ok\n");
      } else {
        Serial.print("check fail\n");
      }

      delay(250);
      return;
    } else {
      Serial.print("trackcv...ok\n");
      trackcv_neural_start(Neural_script_id_emotion);
      inited = true;
      builtInRGB(OFF);
    }
  }

  if (buttonRead(BTN_UP))
  {
    builtInRGB(BLUE);
    new_color = BLUE;
  }
  if (buttonRead(BTN_DOWN))
  {
    builtInRGB(WHITE);
    new_color = WHITE;
  }
  if (buttonRead(BTN_LEFT))
  {
    builtInRGB(YELLOW);
    new_color = YELLOW;
  }
  if (buttonRead(BTN_RIGHT))
  {
    builtInRGB(GREEN);
    new_color = GREEN;
  }

  if(trackcv_neural_count() > 0) {
    if(
      trackcv_neural_class_count(0) > 0 &&
      trackcv_neural_class_p(0, 0) > 80
    ) {
//      Serial.print("face: ");
//      Serial.print(trackcv_neural_x(0));
//      Serial.print(" ");
//      Serial.println(trackcv_neural_y(0));
//      Serial.print("\n");


      if(trackcv_neural_class_p(0,1) == Neural_emotion_HAPPY) { // happy
        builtInRGB(GREEN);
        smile();
//        Serial.print("happy \n");
      } else if (trackcv_neural_class_p(0,1) == Neural_emotion_SAD) { // sad
        sad();
        builtInRGB(RED);
//        Serial.print("sad \n");
      } else if (trackcv_neural_class_p(0,1) == Neural_emotion_ANGER) { // anger
        anger();
        builtInRGB(RED);
//        Serial.print("happy \n");
      } else if (trackcv_neural_class_p(0,1) == 3) { // suprise
//      } else if (trackcv_neural_class_p(0,1) == Neural_emotion_SUPRISE) { // anger
        suprise();
        builtInRGB(GREEN);
//        Serial.print("anger \n");
      } else {
        builtInRGB(BLUE);
        no_emotion();
      }
    }
  } else {

    builtInRGB(OFF);
  }

  delay(100);

  Errno errno = ERR_OK;
  if ((errno = trackcv_get_errno()) != ERR_OK) {
    Serial.print("trackcv err ");
    Serial.println(errno);

    builtInRGB(OFF);

    inited = false;
    return;
  }
}




