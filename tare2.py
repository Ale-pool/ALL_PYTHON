#ejercicio de calificacion
# obtenga una frase del usuario y pidela que te de una letra

frase = input("escribe una frase: ")
Letra = input("escribe una letra: ")
# print(frase.count(Letra)) # cuenta cuantas veces se repite la letra en la frase

frasemin = frase.lower() # convierte la frase en minuscula
letramin = Letra.lower() # convierte la letra en minuscula

# contar el numero de veces que se repite la letra en la frase
listafrase = list(frasemin) # convierte la frase en una lista
print(listafrase)
contador = 0 # inicia el contador en 0
# ciclo for
for caracter in listafrase:
    if caracter == letramin:
        contador = contador + 1

# mostrar el resultado
print(f"la letra {Letra} se repite {contador} veces en la frase {frase}")