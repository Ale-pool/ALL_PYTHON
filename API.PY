import requests
url = "https://pokeapi.co/api/v2/pokemon/"  # se trae la url de la api, en este caso la de los pokemones
pokemon = input("Ingrese el nombre del pokemon: ")  # se pide al usuario que ingrese el nombre del pokemon
response = requests.get(url + pokemon)  # se hace la peticion a la api
data = response.json()


print(f"-----------Movimientos de {pokemon}-----------")
for move in data["moves"]:
    print(move["move"]["name"])  # se imprime el nombre de los movimientos del pokemon  

print(f"-----------Habilidades de {pokemon}-----------")
for type in data["types"]:
    print(type["type"]["name"])  # se imprime el nombre de las habilidades del pokemon

