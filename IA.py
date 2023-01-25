import cv2  #Librerias de OpenCV
import numpy as np #Libreria de Numpy
import serial #Libreria de PySerial
import time # Libreria de Time

cam = cv2.VideoCapture(0)   #Generamos una variable para contener la camara
kernel = np.ones((5,5),np.uint8)

#Variales para almacenar los caracteres que enviaremos al arduino
verde = 'V'
azul = 'A'
rojo = 'R'

#dmesg | grep -v dusconnect | grep -Eo "tty(ACM|USB)." | tail -1  *este es un comando para la consola de linux con la que podemos saber el puerto serial del arduino*
ser = serial.Serial('COM3', 9600)   #Iniciamos y guardamos la comunicacion serial en una variable


def deteccion_verde():

    rangomax = np.array([70, 255, 255]) #Rango maximo de colores en HSV para filtrar los colores verdes
    rangomin = np.array([40, 75, 12])   #Rango minimo de colores en HSV para filtrar los colores verdes
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)   #Cambiamos el filtro de la camara de BGR a HSV
    mascara = cv2.inRange(frameHSV, rangomin, rangomax) #Generamos una mascara que filtrara el color
    opening = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, kernel)
    contorno, _= cv2.findContours(mascara, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) #Buscamos los contornos para los objetos dentro del rango de la mascara
    posibleObjeto = 12000   #Creamos una variable para detectar solo objetos mayores a este tamaño

#Queremos que el programa detecte a partir de cierto tamaño, para esto hacemos un for que pasara por todos los objetos del color de la funcion
    for c in contorno:
        area = cv2.contourArea(c)   #Guardamos el tamaño de los objetos

        if area > posibleObjeto:    #Preguntamos si el tamaño del objeto es mayor al tamaño minimo para ser detectado
            contornoLiso = cv2.convexHull(c)    #Generamos contornos lisos
            cv2.drawContours(frame, [contornoLiso], 0, (0, 255, 0), 3)  #Dibujamos el contorno del objeto
            dato = ser.write(verde.encode('ascii')) #Enviamos el caracter correspondiente por el puerto serial
            print(dato) #Imprimimos en la terminal el bit enviado para checkear que se envio correctamente


#Hacemos el mismo procedimiento para los colores azules y rojos
def deteccion_azul():
    
    rangomax = np.array([125, 255, 255])
    rangomin = np.array([110, 75, 12])
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mascara = cv2.inRange(frameHSV, rangomin, rangomax)
    opening = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, kernel)
    contorno, _ = cv2.findContours(mascara, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    posibleObjeto = 12000

    for c in contorno:
        area = cv2.contourArea(c)

        if area > posibleObjeto:
            contornoLiso = cv2.convexHull(c)
            cv2.drawContours(frame, [contornoLiso], 0, (255, 0, 0), 3)
            dato = ser.write(azul.encode('ascii'))
            print(dato)


'''Para el color rojo debemos hacer dos filtros y unificarlos ya que en la escala HSV el rojo esta al principio y al final de la escala'''
def deteccion_rojo():
    
    #Filtro del comienzo de la escala
    rangomax1 = np.array([5, 255, 255])
    rangomin1 = np.array([0, 75, 12])
    #Filtro del final
    rangomax2 = np.array([180, 255, 255])
    rangomin2 = np.array([170, 75, 12])
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #Hacemos una mascara para cada rango
    mascara1 = cv2.inRange(frameHSV, rangomin1, rangomax1)
    mascara2 = cv2.inRange(frameHSV, rangomin2, rangomax2)
    #Unificamos las mascaras anteriores
    mascaraRoja = cv2.add(mascara1, mascara2)
    opening = cv2.morphologyEx(mascaraRoja, cv2.MORPH_OPEN, kernel)
    contorno, _ = cv2.findContours(mascaraRoja, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    posibleObjeto = 12000

    for c in contorno:
        area = cv2.contourArea(c)

        if area > posibleObjeto:
            contornoLiso = cv2.convexHull(c)
            cv2.drawContours(frame, [contornoLiso], 0, (0, 0, 255), 3)
            dato = ser.write(rojo.encode('ascii'))
            print(dato)


if __name__ == "__main__":
    #Creamos un bucle infinito para correr constantemente el algoritmo
    while True:
        ret, frame = cam.read() #Almacenamos los frames que nos envia la camara

        #Llamamos a las funciones de las detecciones
        deteccion_verde()
        deteccion_azul()
        deteccion_rojo()
        
        cv2.imshow('Camara', frame) #Mostramos en pantalla la imagen que devuelve la camara

        #Por ultimo habilitamos "ESC" como boton que terminara el proceso del programa
        k = cv2.waitKey(1) & 0xFF
        
        if k==27:
            break