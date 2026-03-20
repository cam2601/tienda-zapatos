import cv2
import os

# Carpetas de entrada
carpetas = ["imagenes-mujer", "imagenes-hombre"]

for carpeta in carpetas:
    if not os.path.exists(carpeta):
        print(f"La carpeta {carpeta} no existe, saltando...")
        continue

    carpeta_salida = os.path.join(carpeta, "recortadas")
    os.makedirs(carpeta_salida, exist_ok=True)

    contador = 1  # contador por carpeta para numeración

    for archivo in sorted(os.listdir(carpeta)):  # sorted para mantener orden
        if not archivo.lower().endswith((".png", ".jpg", ".jpeg", ".bmp")):
            continue

        ruta_completa = os.path.join(carpeta, archivo)
        img = cv2.imread(ruta_completa)

        if img is None:
            print(f"No se pudo leer {archivo}, saltando...")
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Threshold automático y contornos para cualquier fondo
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Invertimos si el objeto está oscuro sobre fondo claro
        if cv2.countNonZero(thresh) > (thresh.shape[0]*thresh.shape[1]/2):
            thresh = cv2.bitwise_not(thresh)

        # Encontrar contornos
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            c = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)
            recortada = img[y:y+h, x:x+w]

            nuevo_nombre = f"zapato{contador}.png"
            ruta_salida = os.path.join(carpeta_salida, nuevo_nombre)

            cv2.imwrite(ruta_salida, recortada)
            print(f"Procesado: {archivo} → {nuevo_nombre}")

            contador += 1
        else:
            print(f"No se detectó contenido en {archivo}, saltando...")