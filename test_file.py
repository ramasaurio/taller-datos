# -*- coding: utf-8 -*-
import os

# archivos de lectura
print('hello world')
dataFolder = 'world-cup/'
folders = [folder for folder in os.listdir(dataFolder) if os.path.isdir(dataFolder + folder)]

# archivos para escribir
worldcupPath = 'mundiales.csv'
teamsPath = 'equipos.csv'
matchesPath = 'partidos.csv'

for subFolder in folders:
    files = os.listdir(dataFolder + subFolder)
    for file in [file for file in files if file == 'cup.txt']:
        fullpath = dataFolder + subFolder + '/' + file
        filereader = open(fullpath, 'r')
        for line in filereader:
            line = line.replace(' ', '\n')
            print(line, end='')
        # filereader = open(dataFolder + subFolder + )
    break
