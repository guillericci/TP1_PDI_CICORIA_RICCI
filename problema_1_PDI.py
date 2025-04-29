import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# --- Cargo imagen ------------------------------------------------------------
img_path = os.path.join(os.getcwd(), 'Imagen_con_detalles_escondidos.tif')
img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

if img is None:
    raise ValueError("La imagen no se pudo cargar. Verifica el path o nombre del archivo.")

plt.figure(), plt.imshow(img, cmap='gray', vmin=0, vmax=255), plt.title('Imagen Original'), plt.show(block=False)

# --- Función de ecualización local -------------------------------------------
def ecualizacion_local(imagen, M, N):
    alto, ancho = imagen.shape
    offset_M = M // 2
    offset_N = N // 2

    # Agregar borde para evitar problemas en los bordes
    imagen_bordeada = cv2.copyMakeBorder(imagen, offset_M, offset_M, offset_N, offset_N, borderType=cv2.BORDER_REPLICATE)
    salida = np.zeros_like(imagen)

    # Recorrer toda la imagen y aplicar ecualización local
    for i in range(alto):
        for j in range(ancho):
            ventana = imagen_bordeada[i:i+M, j:j+N]
            hist = cv2.calcHist([ventana], [0], None, [256], [0, 256]).flatten()
            cdf = np.cumsum(hist)
            cdf_normalizada = (cdf - cdf.min()) * 255 / (cdf.max() - cdf.min())
            cdf_normalizada = cdf_normalizada.astype('uint8')
            salida[i, j] = cdf_normalizada[imagen[i, j]]
    return salida

# --- Aplicar ecualización local con distintos tamaños ------------------------
img_3 = ecualizacion_local(img, 3, 3)
img_5 = ecualizacion_local(img, 5, 5)
img_7 = ecualizacion_local(img, 7, 7)
img_9 = ecualizacion_local(img, 9, 9)
img_15 = ecualizacion_local(img, 15, 15)
img_21 = ecualizacion_local(img, 21, 21)
img_31 = ecualizacion_local(img, 31, 31)
img_41 = ecualizacion_local(img, 41, 41)
img_51 = ecualizacion_local(img, 51, 51)


plt.figure(figsize=(12, 10))

plt.subplot(331), plt.imshow(img_3, cmap='gray', vmin=0, vmax=255), plt.title('Ventana 3x3'), plt.axis('off')
plt.subplot(332), plt.imshow(img_5, cmap='gray', vmin=0, vmax=255), plt.title('Ventana 5x5'), plt.axis('off')
plt.subplot(333), plt.imshow(img_7, cmap='gray', vmin=0, vmax=255), plt.title('Ventana 7x7'), plt.axis('off')
plt.subplot(334), plt.imshow(img_9, cmap='gray', vmin=0, vmax=255), plt.title('Ventana 9x9'), plt.axis('off')
plt.subplot(335), plt.imshow(img_15, cmap='gray', vmin=0, vmax=255), plt.title('Ventana 15x15'), plt.axis('off')
plt.subplot(336), plt.imshow(img_21, cmap='gray', vmin=0, vmax=255), plt.title('Ventana 21x21'), plt.axis('off')
plt.subplot(337), plt.imshow(img_31, cmap='gray', vmin=0, vmax=255), plt.title('Ventana 31x31'), plt.axis('off')
plt.subplot(338), plt.imshow(img_41, cmap='gray', vmin=0, vmax=255), plt.title('Ventana 41x41'), plt.axis('off')
plt.subplot(339), plt.imshow(img_51, cmap='gray', vmin=0, vmax=255), plt.title('Ventana 51x51'), plt.axis('off')

plt.tight_layout()
plt.show()


hist_orig = cv2.calcHist([img], [0], None, [256], [0, 256]).ravel()
hist_31 = cv2.calcHist([img_31], [0], None, [256], [0, 256]).ravel()

plt.figure(figsize=(10, 8))
plt.subplot(221), plt.imshow(img, cmap='gray', vmin=0, vmax=255), plt.title('Original'), plt.axis('off')
plt.subplot(222), plt.hist(img.ravel(), 256, [0, 256]), plt.title('Histograma Original')

plt.subplot(223), plt.imshow(img_31, cmap='gray', vmin=0, vmax=255), plt.title('Ecualizada 31x31'), plt.axis('off')
plt.subplot(224), plt.hist(img_31.ravel(), 256, [0, 256]), plt.title('Histograma 31x31')
plt.tight_layout()
plt.show()


histn_31 = hist_31 / hist_31.sum()
cdf_31 = histn_31.cumsum()
plt.plot(cdf_31, color='r')
plt.title('CDF - Ecualización Local 31x31')
plt.grid(True)
plt.show()

# Aplicar filtro de mediana con diferentes tamaños de kernel
img_median3 = cv2.medianBlur(img_31, 3)
img_median5 = cv2.medianBlur(img_31, 5)
img_median7 = cv2.medianBlur(img_31, 7)

# Mostrar resultados
plt.figure(figsize=(10, 5))
ax1 = plt.subplot(221)
plt.imshow(img, cmap='gray')
plt.title('Imagen Original con puntitos')
plt.xticks([]), plt.yticks([])

plt.subplot(222, sharex=ax1, sharey=ax1)
plt.imshow(img_median3, cmap='gray')
plt.title('Filtro de Mediana 3x3')

plt.subplot(223, sharex=ax1, sharey=ax1)
plt.imshow(img_median5, cmap='gray')
plt.title('Filtro de Mediana 5x5')

plt.subplot(224, sharex=ax1, sharey=ax1)
plt.imshow(img_median7, cmap='gray')
plt.title('Filtro de Mediana 7x7')

plt.tight_layout()
plt.show()