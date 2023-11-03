import cv2
import numpy as np
from pyzbar.pyzbar import decode
import sys
import os

def leer_qr(frame, codigos_leidos):
    codigos = decode(frame)
    
    for codigo in codigos:
        try:
            tipo = codigo.type
            datos = codigo.data.decode('utf-8')

            if datos not in codigos_leidos:
                print(f'Tipo: {tipo}, Datos: {datos}')
                codigos_leidos.add(datos)
                out_put(datos)

            puntos = codigo.polygon

            if len(puntos) == 4:
                # Convierte los puntos en una lista de tuplas
                puntos = [(p.x, p.y) for p in puntos]
                puntos = [tuple(map(int, punto)) for punto in puntos]

                # Dibuja un rectángulo alrededor del código QR
                cv2.polylines(frame, [np.array(puntos)], isClosed=True, color=(0, 255, 0), thickness=2)

                # Mostrar en la ventana de la cámara
                cv2.putText(frame, f'Tipo: {tipo}, Datos: {datos}', (puntos[0][0], puntos[0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        except Exception as e:
            print(f"Error al decodificar el código QR: {str(e)}")

    return frame

def main():
    # Redirigir stdout a un archivo temporal para evitar las advertencias
    sys.stdout = open("log.txt", "w")

    cap = cv2.VideoCapture(0)  # Abre la cámara

    if not cap.isOpened():
        print("No se pudo abrir la cámara.")
        return
    
    codigos_leidos = set()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("No se pudo capturar el fotograma.")
            break

        frame_con_qr = leer_qr(frame, codigos_leidos)

        cv2.imshow('Lector de QR', frame_con_qr)
        
        if cv2.waitKey(1) & 0xFF == 27:  # Presiona la tecla Esc para salir
            break

    cap.release()
    cv2.destroyAllWindows()

    # Restaurar la salida estándar original
    sys.stdout.close()
    sys.stdout = sys.__stdout__

def out_put(datos):
    filename = 'qrcodes.txt'
    if not os.path.exists(filename):
        with open(filename, 'w') as file:
            file.write(datos)
    else:
        with open(filename, 'r') as file:
            existing_data = file.read()
        if datos not in existing_data:
            with open(filename, 'a') as file:
                file.write('\n' + datos)

if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    sys.exit()
  except Exception as e:
      from tkinter import messagebox
      messagebox.showerror(title="lector qr de la camara", message=f"{e}")
