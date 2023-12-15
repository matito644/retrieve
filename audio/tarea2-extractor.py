# CC5213 - TAREA 2
# 28 de septiembre de 2023
# Alumno: Matías Rivera Contreras

import sys
import os.path
import subprocess
import librosa
import numpy


def convertir_a_wav(archivo_audio, sample_rate, dir_temporal):
    archivo_wav = "{}/{}.{}.wav".format(dir_temporal, os.path.basename(archivo_audio), sample_rate)
    archivo_wav_temp = "{}/{}.{}.{}.wav".format(dir_temporal, os.path.basename(archivo_audio), sample_rate, "temp")
    # verificar si ya esta creado
    if os.path.isfile(archivo_wav):
        return archivo_wav
    comando = ["ffmpeg", "-i", archivo_audio, "-filter:a", "dynaudnorm=p=0.95:s=5", "-ac", "1", "-ar", str(sample_rate), archivo_wav]
    print("INICIANDO: {}".format(" ".join(comando)))
    proc = subprocess.run(comando, stderr=subprocess.STDOUT)
    if proc.returncode != 0:
        raise Exception("Error ({}) en comando: {}".format(proc.returncode, " ".join(comando)))
    return archivo_wav


def tarea2_extractor(dir_audios, dir_descriptores):
    if not os.path.isdir(dir_audios):
        print("ERROR: no existe directorio {}".format(dir_audios))
        sys.exit(1)
    elif os.path.exists(dir_descriptores):
        print("ERROR: ya existe directorio {}".format(dir_descriptores))
        sys.exit(1)

    sample_rate = 22050
    samples_por_ventana = 4096
    # leer archivos de audio .m4a en dir_audios
    list_with_mp4 = []
    for audio in sorted(os.listdir(dir_audios)):
        archivo_m4a = "{}/{}".format(dir_audios, audio)
        list_with_mp4.append(archivo_m4a)
    # crear dir_descriptores
    os.makedirs(dir_descriptores, exist_ok=True)
    # cada audio convertirlo a wav
    for audio in list_with_mp4:
        convertir_a_wav(audio, sample_rate, dir_descriptores)
    # cargar cada archivo wav y calcular descriptores
    index = 1
    for wav in sorted(os.listdir(dir_descriptores)):
        archivo_wav = "{}/{}".format(dir_descriptores, wav)
        samples, sr = librosa.load(archivo_wav, sr=sample_rate)
        # calcular MFCC
        mfcc = librosa.feature.mfcc(y=samples, sr=sr, n_mfcc=40, n_fft=samples_por_ventana, hop_length=samples_por_ventana)
        # quitar los primeros coeficientes
        mfcc = mfcc[4:]
        descriptores = mfcc.transpose()
        numpy.savetxt(dir_descriptores+wav+'.txt', descriptores)
        # guardar nombre del archivo y el inicio de la ventana
        with open(dir_descriptores + "archivoTiempos.txt", "a") as f:
            for i in range(0, samples_por_ventana * descriptores.shape[0], samples_por_ventana):
                # tiempo de inicio de la ventana
                ventana_inicio = i / sample_rate
                not_name = len('.'+str(sample_rate)+'.wav')
                nombre_archivo = wav[:-not_name]
                f.write(str(index) + '\t' + nombre_archivo + "\t" + str(ventana_inicio) + "\n")
                index+=1
            f.close()

# inicio de la tarea
if len(sys.argv) < 3:
    print("Uso: {} [dir_audios] [dir_descriptores]".format(sys.argv[0]))
    sys.exit(1)

dir_audios = sys.argv[1]
dir_descriptores = sys.argv[2]

tarea2_extractor(dir_audios, dir_descriptores)
