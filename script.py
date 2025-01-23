
# si queremos multplicar dos numeros dados por el usuario y mostrar el resultado
# debemos hacer lo siguiente
import math

num1 = int(input("Ingrese el primer numero: "))
num2 = int(input("Ingrese el segundo numero: "))

resultado = num1 * num2

raiz = math.sqrt(resultado)

print(f"El resultado de la multiplicacion es: {resultado}")
print(f"La raiz cuadrada del resultado es: {raiz}")

answers = [resultado, raiz]

type(answers)