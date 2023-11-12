import cv2
import tkinter as tk
from tkinter import filedialog
from pyzbar.pyzbar import decode
import sys
from tkinter import messagebox

def leer_barcodes(imagen, codigos_leidos):
    codigos = decode(imagen)
    
    for codigo in codigos:
        tipo = codigo.type
        datos = codigo.data.decode('utf-8')
        
        if datos not in codigos_leidos:
            print(f'Tipo: {tipo}, Datos: {datos}')
            codigos_leidos.add(datos)

        rect = codigo.rect

        # Dibuja un rectángulo alrededor del código de barras
        cv2.rectangle(imagen, (rect.left, rect.top), (rect.left + rect.width, rect.top + rect.height), (0, 255, 0), 2)

        # Muestra el resultado en la imagen
        cv2.putText(imagen, f'Tipo: {tipo}, Datos: {datos}', (rect.left, rect.top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return imagen

def abrir_archivo():
    ruta_imagen = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png *.jpg")])

    if ruta_imagen:
        imagen = cv2.imread(ruta_imagen)

        if imagen is None:
            print("No se pudo cargar la imagen.")
            return
        
        codigos_leidos = set()

        imagen_con_barcodes = leer_barcodes(imagen, codigos_leidos)

        cv2.imshow('Lector de Códigos de Barras', imagen_con_barcodes)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def main():
    ventana = tk.Tk()
    ventana.geometry("300x100")
    boton_abrir = tk.Button(ventana, text="Abrir archivo", command=abrir_archivo)
    boton_abrir.pack()

    ventana.mainloop()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        messagebox.showerror(title="lector qr de archivos", message=f"{e}")
