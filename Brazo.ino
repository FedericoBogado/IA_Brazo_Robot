#include <Servo.h> //Libreria de los servos

#define DELAY 8000 //Delay de 8 segundos para cada vez que comienza a ejecutar una serie de movimientos

unsigned long tiempoActual = 0; //variable para actualizar el contador de millis

//Declaracion de servos
Servo servoBase;
Servo servoTronco;
Servo servoPinza;

char color; //Variable de tipo caracter para almacenar la informacion de la camara a traves del puerto serial

//Flags para la habilitacion de los movimientos segun el color. (1 = True y 0 = False)
bool verde_up = 1;
bool azul_up = 1;
bool rojo_up = 1;

//Aca declaramos las funciones en donde estaran los movimientos de los servos
void base();
void servosVerde();
void servosAzul();
void servosRojo();

void setup() {
  Serial.begin(9600); //Iniciamos el puerto serial con una velocidad de 9600 baudios

    //Declaramos los pines digitales a los que se conectaran los servos
  servoBase.attach(8);
  servoTronco.attach(9);
  servoPinza.attach(10);

  base(); //Hacemos que el brazo comience en la posicion inicial al prender el arduino
}

void loop() {
  if (Serial.available()){ //Si esta disponible la comunicacion serial:
    color = Serial.read(); //Actualizamos la informacion serial
    
    switch (color){
      
     case 'V':
      if (verde_up == 1){ //Preguntamos si el color esta habilitado
       //Deshabilitamos las flags
       verde_up = 0;
       azul_up = 0;
       rojo_up = 0;
       servosVerde(); //Ejecutamos el movimiento de los para el color
    }
    break;
    
    case 'A':
      if (azul_up == 1){
       azul_up = 0;
       verde_up = 0;
       rojo_up = 0;
       servosAzul();
    }
    break;
    
    case 'R':
      if (rojo_up == 1){
       rojo_up = 0;
       azul_up = 0;
       verde_up = 0;
       servosRojo();
    }
    break;
    
      default:
        break;
   }

    //pasado el delay queremos que el brazo pueda volver a responder segun el puerto serial
   if(millis() > tiempoActual + DELAY){ //Preguntamos si paso mas tiempo que el delay
    tiempoActual = millis(); //Actualizamos el cronometro
    //Volvemos a habilitar las flags
    verde_up = 1;
    azul_up = 1;
    rojo_up = 1;
   }
  }
}

//Set de movimientos para la posicion de espera
void base(){
  servoBase.write(75); //Movemos el servo 75 grados
  delay(1000); //Le damos un delay de un segundo entre movimiento y movimiento
  servoTronco.write(90);
  delay(1000);
  servoPinza.write(130);
  delay(1000);
}

//Set de movimientos para el color verde
 void servosVerde(){
    servoBase.write(0);
    delay(1000);
    servoTronco.write(140);
    delay(1000);
    servoBase.write(180);
    delay(1000);
    base();
}

//Set de movimientos para el color Azul
void servosAzul(){
    servoBase.write(180);
    delay(1000);
    servoTronco.write(140);
    delay(1000);
    servoBase.write(0);
    delay(1000);
    base();
}

//Set de movimientos para el color rojo
void servosRojo(){
    servoPinza.write(90);
    delay(1000);
    servoTronco.write(140);
    delay(1000);
    servoPinza.write(180);
    delay(1000);
    base();
}
