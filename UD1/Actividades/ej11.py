#Crea una aplicació que vaja llegint operacions d’un fitxer (una operació per línia) i
#afegisca els resultats. Per exemple, si llig: 4 + 4
#Haurà de generar: 4 + 4 = 8
#Utilitza funcions anònimes per a implementar les operacions

import os

operaciones = os.path.join(os.path.dirname(__file__), "operaciones.txt")
result = os.path.join(os.path.dirname(__file__), "resultados.txt")

suma = lambda x, y: x + y
resta = lambda x, y: x - y
multiplicar = lambda x, y: x * y
dividir = lambda x, y: x / y


def readinfo(file):
    
	filas = []
	with open(file, 'r') as f:
     
		for i in f:
      
			operacion = i.split(" ")
   
			x = int(operacion[0])
			y = int(operacion[2])
   
			if operacion[1] == "+":
				res = suma(x, y)
			if operacion[1] == "-":
				res = resta(x, y)
			if operacion[1] == "*":
				res = multiplicar(x, y)
			if operacion[1] == "/":
				res = dividir(x, y)
    
			add = str(str(operacion[0])+" "+str(operacion[1])+" "+str(operacion[2].replace("\n", " "))+"= "+str(res) + "\n")
			filas.append(add)
   
		f.close()
  
	guardar(filas)


def guardar(lineas):
	with open(result, 'w') as fi:
		fi.writelines(lineas)


readinfo(operaciones)