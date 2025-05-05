from copy import deepcopy


class Sudokudjoku:
    def __init__(self, izgled=None):
        self.izgled = izgled
        self.djeca = []


def provjera_pune_table(tabla):
    for red in tabla:
        if 0 in red:
            return False
    return True


def provjera_postojanja_2(tabla, n=4):
    for i in range(n):
        red = tabla[i]
        for j in range(n):
            if red.count(red[j]) > 1 and red[j] != 0:
                return False

    for i in range(n):
        for j in range(n):
            element = tabla[i][j]
            for k in range(i + 1, n):
                element2 = tabla[k][j]
                if element == element2 and element != 0:
                    return False

    for i in range(0, n, 2):
        for j in range(0, n, 2):
            box = []
            for x in range(i, i + 2):
                for y in range(j, j + 2):
                    if tabla[x][y] != 0 and tabla[x][y] in box:
                        return False
                    box.append(tabla[x][y])
    return True


def sve_kombinacije(cvor, n=4):
    rjesenja = []
    stek = [cvor]
    while stek:
        trenutni_cvor = stek.pop(0)
        if provjera_pune_table(trenutni_cvor.izgled):
            if provjera_postojanja_2(trenutni_cvor.izgled) and all(trenutni_cvor.izgled != r for r in rjesenja):
                rjesenja.append(deepcopy(trenutni_cvor.izgled))
            continue
        for i in range(n):
            for j in range(n):
                if trenutni_cvor.izgled[i][j] == 0:
                    for m in range(1, n + 1):
                        novi_cvor = deepcopy(trenutni_cvor)
                        novi_cvor.izgled[i][j] = m
                        if provjera_postojanja_2(novi_cvor.izgled):
                            stek.append(novi_cvor)
                            trenutni_cvor.djeca.append(novi_cvor)
    return rjesenja


def pomoc(u):
    moguci_brojevi = []
    print("Za koje polje zelite pomoc?")
    x = int(input("X koordinata:"))
    y = int(input("Y koordinata:"))
    if u:
        for resenja in u:
            moguci_brojevi.append(resenja[x][y])
        print("Moguci brojevi na tom polju je/su:", *moguci_brojevi)
    else:
        print("Ne postoje dobri brojevi na tom mjestu")


def unos_manuelno():
    m = int(input("Velicina table: "))
    tabela = []
    print("Unesite pocetno stanje matrice:")
    for i in range(m):
        red = [int(x) for x in input().split()]
        tabela.append(red)

    return m, tabela


def unos_fajl(file):
    tabela = []
    with open(file, "r") as datoteka:
        m = int(datoteka.readline())
        for roww in datoteka:
            roww = roww.strip("\n")
            redovi = list(roww)
            for i in range(len(redovi)):
                redovi[i] = int(redovi[i])
            tabela.append(redovi)
    return m, tabela


def pocetak():
    print("---DOBRODOSLI U IGRU SUDOKU---\n\nOdaberite jednu od opcija za unos:")
    odluka = int(input("1. Manuelan unos podataka\n2. Unos putem text fajla\n"))
    if odluka == 1:
        m, tabela = (unos_manuelno())

    elif odluka == 2:
        file = input("Unesite naziv fajla:\n")
        try:
            m, tabela = unos_fajl(file)
        except FileNotFoundError:
            print("Fajl ne postoji")
            exit()
    else:
        print("NEPRAVILAN UNOS")
        exit()

    return m, tabela


def igrac_igra(tabla, igra_tabla, broj, x, y):
    if tabla[x][y] == 0:
        igra_tabla[x][y] = broj
    return igra_tabla


def na_dobrom_putu(u, igrac_tabla):
    for matrica in u:
        pogodak = True
        for i in range(4):
            for j in range(4):
                if igrac_tabla[i][j] != 0 and matrica[i][j] != igrac_tabla[i][j]:
                    pogodak = False
                    break
            if not pogodak:
                break
        if pogodak:
            return True
    return False


def uspjesna_igra(igrac_tabla, u):
    for matrica in u:
        if all(matrica[i][j] == igrac_tabla[i][j] for i in range(4) for j in range(4)):
            return True
    return False


n, tabla = pocetak()
igra_tabla = deepcopy(tabla)
cvor = Sudokudjoku(tabla)
u = sve_kombinacije(cvor)

while True:
    print("---MENI---\n\n1.Unesi broj\n2.Pomoc\n3.Ispis staba\n4.Rjesenje\n5.Nema rjesenja\n6.Zavrsi program")
    t = int(input())
    if t == 1:
        for row in igra_tabla:
            print(row)
        x = int(input("Unesite x koordinatu:"))
        y = int(input("Unesite y koordinatu:"))
        broj = int(input("Unesite broj:"))
        igra_tabla = igrac_igra(tabla, igra_tabla, broj, x, y)
        if uspjesna_igra(igra_tabla, u):
            print("Rijesili ste igru")
            break
    elif t == 2:
        if na_dobrom_putu(u, igra_tabla):
            print("Na dobrom ste putu")
            continue
        else:
            print("Na losem ste putu")
            pomoc(u)
    elif t == 3:
        pass
    elif t == 4:
        pass
    elif t == 5:
        if len(u) == 0:
            print("Sudoku nema rjsenja :)")
            break
        else:
            print("Losa procjena. Igra ima rjsenje")
    elif t == 6:
        break
    else:
        print("NEPRAVILAN UNOS")
        exit()
