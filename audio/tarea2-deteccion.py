# CC5213 - TAREA 2
# 28 de septiembre de 2023
# Alumno: Matías Rivera Contreras

import sys
import os.path


def tarea2_deteccion(dir_resultados_knn, file_resultados_txt):
    if not os.path.isdir(dir_resultados_knn):
        print("ERROR: no existe directorio {}".format(dir_resultados_knn))
        sys.exit(1)
    elif os.path.exists(file_resultados_txt):
        print("ERROR: ya existe archivo {}".format(file_resultados_txt))
        sys.exit(1)

    sample_rate = 22050
    samples_por_ventana = 4096
    slice = samples_por_ventana/sample_rate
    # leer resultados de knn en dir_resultados_knn
    [resultados_knn] = os.listdir(dir_resultados_knn)
    with open(dir_resultados_knn + resultados_knn, 'r') as f:
        all = []
        while True:
            line = f.readline()
            if not line:
                break
            split = line.split('\t')
            init_q = float("{:.4f}".format(float(split[2])))
            init_r = float("{:.4f}".format(float(split[4])))
            difference = float("{:.2f}".format(init_q-init_r))
            all.append([split[1], init_q, split[3], init_r, difference])
        f.close()
    # buscar secuencias similares entre audios
    # primero los ordenamos según radio, canción y diferencia de tiempo
    sorted_all = sorted(all, key=lambda x:(x[0],x[2],x[4]))
    # vamos llevamos la cuenta de los elementos que hemos visto
    combinations = []
    grouped = []
    for i in sorted_all:
        element = [i[0], i[2], i[4]]
        if combinations == [] or element != combinations[-1]:
            combinations.append(element)
            # se agrega el elemento con un contador que parte en cero
            grouped.append(i+[0])
        else:
            # siempre queda al final el elemento recién agregado y las repeticiones vienen seguidas
            # pues hubo un ordenamiento previo
            grouped[-1][-1] += 1
    # seleccionamos los que efectivamente van a retornarse
    selected = []
    for i in grouped:
        # si apareció al menos poco más de un segundo
        if i[-1] >= 7:
            selected.append(i)

    # escribir en file_resultados_txt las detecciones encontradas
    # según el formato: print("{}\t{}\t{}\t{}\t{}".format(radio, desde, largo, cancion, confianza))
    with open(file_resultados_txt, 'w') as ff:
        for i in selected:
            print("{}\t{}\t{}\t{}\t{}".format(i[0], i[1], slice*i[5], i[2], i[5]), file=ff)


# inicio de la tarea
if len(sys.argv) < 3:
    print("Uso: {} [dir_resultados_knn] [file_resultados_txt]".format(sys.argv[0]))
    sys.exit(1)

dir_resultados_knn = sys.argv[1]
file_resultados_txt = sys.argv[2]

tarea2_deteccion(dir_resultados_knn, file_resultados_txt)
