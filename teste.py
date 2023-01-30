f = open("stands_pt3.txt", "r")

lista_stands = []
for stand in f:
    lista_stands.append(stand.replace("\n", "").split(','))

print(lista_stands)