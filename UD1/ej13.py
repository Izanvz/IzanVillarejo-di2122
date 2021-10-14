#Activitat 13 Anem a implementar un xicotet joc per consola. El programa generarà un número
#aleatori entre 0 i 100 (utilitzeu randint() del mòdul random) i demanarà a l’usuari que introduïsca un
#número.
#Mentre el número siga massa menut, llançarà una excepció ErrorEnterMassaMenut indicant-li-ho. Si
#per contra és massa gran llançarà ErrorEnterMassaGran.
#El joc acabarà quan s’introduïsca un valor no numèric o quan s’introduïsca l’enter buscat, en este cas
#felicitarà a l’usuari.
import random


random_num = random.randint(0, 100)

print(random_num)

class ErrorMuyGrande(Exception):
    pass


class ErrorMuyPequeño(Exception):
	pass

while True:
        
    x = int(input("Dime un numero: "))
        
    try:
    
        if x == random_num:
            print("Enhorabuena as adivinado el numero aleatorio")
            break
        if x < random_num:
            raise ErrorMuyPequeño
        if x > random_num:
            raise ErrorMuyGrande
        
        
    except ValueError:
        print("Saliendo, valor no numérico")
        break    
    except ErrorMuyPequeño:
	    print("El numero es pequeño")
    except ErrorMuyGrande:
        print("El numero es grande")