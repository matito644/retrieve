# CC5213 - TAREA 2
# 28 de septiembre de 2023
# Alumno: Matías Rivera Contreras

import sys
import os.path
import numpy
import scipy


def tarea2_busqueda(dir_descriptores_q, dir_descriptores_r, dir_resultados_knn):
    if not os.path.isdir(dir_descriptores_q):
        print("ERROR: no existe directorio {}".format(dir_descriptores_q))
        sys.exit(1)
    elif not os.path.isdir(dir_descriptores_r):
        print("ERROR: no existe directorio {}".format(dir_descriptores_r))
        sys.exit(1)
    elif os.path.exists(dir_resultados_knn):
        print("ERROR: ya existe archivo {}".format(dir_resultados_knn))
        sys.exit(1)
    # leer descriptores de Q de dir_descriptores_q
    all_des_q = []
    for archivo in sorted(os.listdir(dir_descriptores_q)):
        if not archivo.endswith(".txt") or archivo.endswith("archivoTiempos.txt"):
            continue
        des_q = numpy.loadtxt(dir_descriptores_q + archivo)
        if len(all_des_q) == 0:
            all_des_q = des_q
        else:
            all_des_q = numpy.vstack([all_des_q, des_q])
    # leer descriptores de R de dir_descriptores_r
    all_des_r = []
    for archivo in sorted(os.listdir(dir_descriptores_r)):
        if not archivo.endswith(".txt") or archivo.endswith("archivoTiempos.txt"):
            continue
        des_r = numpy.loadtxt(dir_descriptores_r + archivo)
        if len(all_des_r) == 0:
            all_des_r = des_r
        else:
            all_des_r = numpy.vstack([all_des_r, des_r])

    # matriz_distancias, para cada descriptor q localizar el mas cercano en R
    matriz_distancias = scipy.spatial.distance.cdist(all_des_q, all_des_r, metric='euclidean')
    # crear dir_resultados_knn
    os.makedirs(dir_resultados_knn, exist_ok=True)
    with open(dir_descriptores_q + "archivoTiempos.txt", "r") as fq:
        times_q = []
        while True:
            line = fq.readline()
            if not line:
                break
            split = line.split('\t')
            times_q.append(split)
        fq.close()

    with open(dir_descriptores_r + "archivoTiempos.txt", "r") as fr:
        times_r = []
        while True:
            line = fr.readline()
            if not line:
                break
            split = line.split('\t')
            times_r.append(split)
        fr.close()

    # escribir los knn en dir_resultados_knn
    # incluyendo los tiempos que representa cada ventana de q y r
    posicion_min = numpy.argmin(matriz_distancias, axis=1)
    with open(dir_resultados_knn + "resultados_knn.txt", 'w') as ff:
        for i in range(len(times_q)):
            print(times_q[i][0] + '\t' + times_q[i][1] + '\t' + times_q[i][2][:-2] + '\t' + times_r[posicion_min[i]][1] + '\t' + times_r[posicion_min[i]][2], end='', file=ff)
        ff.close()


# inicio de la tarea
if len(sys.argv) < 4:
    print("Uso: {} [dir_descriptores_q] [dir_descriptores_r] [dir_resultados_knn]".format(sys.argv[0]))
    sys.exit(1)

dir_descriptores_q = sys.argv[1]
dir_descriptores_r = sys.argv[2]
dir_resultados_knn = sys.argv[3]

tarea2_busqueda(dir_descriptores_q, dir_descriptores_r, dir_resultados_knn)
