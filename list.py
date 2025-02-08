# En esta ocacion vamos a ver como se pueden crear listas en python
# uana lista en py es una lista de elementos que se pueden agregar y eliminar
# se pueden crear listas vacias o con elementos
# las listas en python son mutables, es decir se pueden modificar
# las listas en python son indexadas, es decir se pueden acceder a los elementos de la lista mediante su indice
# las listas en python son ordenadas, es decir se pueden ordenar los elementos de la lista
# las listas en python son homogeneas, es decir se pueden tener elementos de diferentes tipos
# las listas en python son anidadas, es decir se pueden tener listas dentro de listas

# Crear una lista vacia
carro = ["juan"]

# Crear una lista con elementos
padres = ["mama", "papa"]

# Crear una lista con elementos de diferentes tipos

animales = ["gato", "perro", "elefante"]

# Crear una lista anidada
personas = [["mama", "papa"], ["hermano", "hermana"]]

print(personas)

# Crear una lista con elementos de diferentes tipos
letra = "ALEX"
lista = list(letra)
print(lista[2])


# trocear una lista
# el trociado de una lista es una forma de obtener una parte de la lista

casa = ["sala", "comedor", "cocina", "recamara", "baño","patio"]
casaa = casa[::-1] # obtiene los elementos de la lista desde el indice 2 hasta el indice 4
print(casaa)

# si queremos saber otra manera de rebertir una lista se puede

familia = ["mama", "papa", "hermano", "hermana"]
familia.reverse()
print(familia)

