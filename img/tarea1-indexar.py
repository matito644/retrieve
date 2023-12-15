# CC5213 - TAREA 1 - RECUPERACIÓN DE INFORMACIÓN MULTIMEDIA
# 15 de agosto de 2023
# Alumno: Matías Rivera C.

import sys
import os.path
import cv2
import scipy
import numpy

# el descriptor va a ser el vector de intensidades, ecualizando la imagen
# y aplicando cierto desenfoque
def vector_de_intensidades(archivo_imagen):
    imagen_1 = cv2.imread(archivo_imagen, cv2.IMREAD_GRAYSCALE)
    imagen_1 = cv2.equalizeHist(imagen_1)
    imagen_1 = cv2.GaussianBlur(imagen_1, (5, 5), 0, 0)
    imagen_1 = cv2.resize(imagen_1, (20, 20), interpolation=cv2.INTER_AREA)
    descriptor_imagen = imagen_1.flatten()
    return descriptor_imagen


def tarea1_indexar(dir_input_imagenes_R, dir_output_descriptores_R):
    if not os.path.isdir(dir_input_imagenes_R):
        print("ERROR: no existe directorio {}".format(dir_input_imagenes_R))
        sys.exit(1)
    elif os.path.exists(dir_output_descriptores_R):
        print("ERROR: ya existe directorio {}".format(dir_output_descriptores_R))
        sys.exit(1)
    os.makedirs(dir_output_descriptores_R, exist_ok=True)

    lista_nombres = []
    matriz_descriptores_vector = []
    # calcular el descriptor para cada imagen y almacenarlo con el resto
    for nombre in os.listdir(dir_input_imagenes_R):
        if not nombre.endswith(".jpg"):
            continue
        archivo_imagen = "{}/{}".format(dir_input_imagenes_R, nombre)
        descriptor_vector = vector_de_intensidades(archivo_imagen)
        if len(matriz_descriptores_vector) == 0:
            matriz_descriptores_vector = descriptor_vector
        else:
            matriz_descriptores_vector = numpy.vstack([matriz_descriptores_vector, descriptor_vector])
        lista_nombres.append(nombre)
    # guardar los descriptores y los nombres
    numpy.savetxt(dir_output_descriptores_R+'descriptores_vector.txt', matriz_descriptores_vector)
    with open(dir_output_descriptores_R + 'nombres.txt','w') as file:
	       file.write('\n'.join(lista_nombres))

if len(sys.argv) < 3:
    print("Uso: {} [dir_input_imagenes_R] [dir_output_descriptores_R]".format(sys.argv[0]))
    sys.exit(1)

dir_input_imagenes_R = sys.argv[1]
dir_output_descriptores_R = sys.argv[2]

tarea1_indexar(dir_input_imagenes_R, dir_output_descriptores_R)