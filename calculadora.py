import math

# VAMOS A REALIZAR UNA CALCULADORA
# Vamos a realizar una calculadora que realice las siguientes operaciones:
# 1. Suma
# 2. Resta
# 3. Multiplicación
# 4. División
# 5. Raiz cuadrada

# Vamos a pedir dos numeros

num1 = int(input(" Ingrese el primer numero: "))
num2 = int(input(" Ingrese el segundo numero: "))
operacion = input("Ingrese la operacion que desea realizar 1.Suma 2.Resta 3.Multiplicacion 4.Division 5.Raiz cuadrada:")

if operacion == "1":
    print(f"El resultado de la suma es: {num1 + num2}")
elif operacion == "2":
    print(f"El resultado de la resta es: {num1 - num2}")
elif operacion == "3":
    print(f"El resultado de la multiplicacion es: {num1 * num2}")
elif operacion == "4":
    print(f"El resultado de la division es: {num1 / num2}")
elif operacion == "5":
    print(f"El resultado de la raiz cuadrada es: {math.sqrt(num1)}")
elif operacion	== "6":
    print(f"El resultado de la potencia es: {num1 ** num2}")

