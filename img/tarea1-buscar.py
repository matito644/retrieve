# CC5213 - TAREA 1 - RECUPERACIÓN DE INFORMACIÓN MULTIMEDIA
# 15 de agosto de 2023
# Alumno: Matías Rivera C.

import sys
import os.path
import cv2
import scipy
import numpy

# el descriptor va a ser el vector de intensidades, ecualizando la imagen
# y dando la opción de aplicar un flip a la imagen
def vector_de_intensidades(archivo_imagen, flipped = False):
    imagen = cv2.imread(archivo_imagen, cv2.IMREAD_GRAYSCALE)
    if flipped:
        imagen = cv2.flip(imagen, 1)
    imagen = cv2.equalizeHist(imagen)
    imagen = cv2.resize(imagen, (20, 20), interpolation=cv2.INTER_AREA)
    descriptor_imagen = imagen.flatten()
    return descriptor_imagen


def tarea1_buscar(dir_input_imagenes_Q, dir_input_descriptores_R, file_output_resultados):
    if not os.path.isdir(dir_input_imagenes_Q):
        print("ERROR: no existe directorio {}".format(dir_input_imagenes_Q))
        sys.exit(1)
    elif not os.path.isdir(dir_input_descriptores_R):
        print("ERROR: no existe directorio {}".format(dir_input_descriptores_R))
        sys.exit(1)
    elif os.path.exists(file_output_resultados):
        print("ERROR: ya existe archivo {}".format(file_output_resultados))
        sys.exit(1)

    lista_nombres_q = []
    matriz_descriptores_q = []
    matriz_descriptores_flip_q = []
    # para cada imagen se calcula su descriptor y el descriptor de la imagen con un flip
    for nombre in os.listdir(dir_input_imagenes_Q):
        if not nombre.endswith(".jpg"):
            continue
        archivo_imagen = "{}/{}".format(dir_input_imagenes_Q, nombre)
        descriptor_vector_q = vector_de_intensidades(archivo_imagen)
        descriptor_vector_flip = vector_de_intensidades(archivo_imagen, True)
        if len(matriz_descriptores_q) == 0:
            matriz_descriptores_q = descriptor_vector_q
            matriz_descriptores_flip_q = descriptor_vector_flip
        else:
            matriz_descriptores_q = numpy.vstack([matriz_descriptores_q, descriptor_vector_q])
            matriz_descriptores_flip_q = numpy.vstack([matriz_descriptores_flip_q, descriptor_vector_flip])
        lista_nombres_q.append(nombre)

    # cargar los descriptores y los nombres de las imágenes originales
    matriz_descriptores_vector_r = numpy.loadtxt(dir_input_descriptores_R + 'descriptores_vector.txt')
    with open(dir_input_descriptores_R + 'nombres.txt','r') as file:
           lista_nombres_r = file.read().split('\n')

    with open(file_output_resultados, 'w') as f:
        i = 0
        # para cada uno de los descriptores calculados antes se busca el descriptor más cercano de alguna imagen original
        for descriptor, descriptor_flip in zip(matriz_descriptores_q, matriz_descriptores_flip_q):
            matriz_distancia = scipy.spatial.distance.cdist(matriz_descriptores_vector_r, numpy.reshape(descriptor, (1, -1)), metric='cityblock')
            matriz_distancia_flip = scipy.spatial.distance.cdist(matriz_descriptores_vector_r, numpy.reshape(descriptor_flip, (1, -1)), metric='cityblock')

            # obtener el mínimo valor y la posición del mismo
            matriz_distancia = numpy.concatenate(matriz_distancia, axis=None)
            posicion_minima = numpy.argmin(matriz_distancia)
            valor_minimo = numpy.amin(matriz_distancia)

            matriz_distancia_flip = numpy.concatenate(matriz_distancia_flip, axis=None)
            posicion_minima_flip = numpy.argmin(matriz_distancia_flip)
            valor_minimo_flip = numpy.amin(matriz_distancia_flip)
            
            if valor_minimo <= valor_minimo_flip:
                print("{}\t{}\t{}".format(lista_nombres_q[i], lista_nombres_r[posicion_minima], valor_minimo), file=f)
            else:
                print("{}\t{}\t{}".format(lista_nombres_q[i], lista_nombres_r[posicion_minima_flip], valor_minimo_flip), file=f)
            i += 1


# inicio de la tarea
if len(sys.argv) < 4:
    print("Uso: {} [dir_input_imagenes_Q] [dir_input_descriptores_R] [file_output_resultados]".format(sys.argv[0]))
    sys.exit(1)

dir_input_imagenes_Q = sys.argv[1]
dir_input_descriptores_R = sys.argv[2]
file_output_resultados = sys.argv[3]

tarea1_buscar(dir_input_imagenes_Q, dir_input_descriptores_R, file_output_resultados)
