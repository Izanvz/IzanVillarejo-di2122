#Crea una aplicació que vaja llegint operacions d’un fitxer (una operació per línia) i
#afegisca els resultats. Per exemple, si llig: 4 + 4
#Haurà de generar: 4 + 4 = 8
#Utilitza funcions anònimes per a implementar les operacions

import os

operaciones = os.path.join(os.path.dirname(__file__), "operaciones.txt")
res = os.path.join(os.path.dirname(__file__), "res.txt")

suma = lambda x, y: x + y
resta = lambda x, y: x - y
multiplicar = lambda x, y: x * y
dividir = lambda x, y: x / y


def leer(archivo):
	lineas = []
	with open(archivo, 'r') as f:
		for linea in f:
			operacion = linea.split(" ")
			x = int(operacion[0])
			y = int(operacion[2])
			if operacion[1] == "+":
				op = suma(x, y)
			elif operacion[1] == "-":
				op = resta(x, y)
			elif operacion[1] == "*":
				op = multiplicar(x, y)
			elif operacion[1] == "/":
				op = dividir(x, y)
			add = str(str(operacion[0]) + " " + str(operacion[1]) + " " + str(operacion[2].replace("\n", " ")) + "= " + str(
				op) + "\n")
			lineas.append(add)
		f.close()
	saveFile(lineas)


def saveFile(lineas):
	with open(res, 'w') as fi:
		fi.writelines(lineas)


leer(operaciones)