num = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]

def impares(x):
    if x%2==0:
        return False
    else:
        return True

impar = filter(impares, num)

def pares(x):
    if x%2==0:
        return True
    else:
        return False

par = filter(pares, num)

print("Pares")
for x in par:
  print(x)
  
print("Impares")
for x in impar:
  print(x)