import json

film = []

# -----------------------
# INSERIRE FILM
# -----------------------
def inserisci_film():
    nome = input("Nome film: ")
    anno = int(input("Anno uscita: "))
    incasso = float(input("Incasso al botteghino: "))

    nuovo = {
        "nome": nome,
        "anno": anno,
        "incasso": incasso
    }

    film.append(nuovo)


# -----------------------
# VISUALIZZARE FILM
# -----------------------
def mostra_film():
    for i, f in enumerate(film):
        print(i, "-", f["nome"], f["anno"], f["incasso"])


# -----------------------
# MODIFICARE FILM
# -----------------------
def modifica_film():
    mostra_film()
    i = int(input("Indice del film da modificare: "))

    film[i]["nome"] = input("Nuovo nome: ")
    film[i]["anno"] = int(input("Nuovo anno: "))
    film[i]["incasso"] = float(input("Nuovo incasso: "))


# -----------------------
# CANCELLARE FILM
# -----------------------
def cancella_film():
    mostra_film()
    i = int(input("Indice del film da cancellare: "))
    film.pop(i)


# =======================
# SALVATAGGIO CON SEPARATORE
# =======================
def salva_separatore():
    f = open("film.txt", "w")

    for x in film:
        riga = x["nome"] + ";" + str(x["anno"]) + ";" + str(x["incasso"])
        f.write(riga + "\n")

    f.close()


def carica_separatore():
    try:
        f = open("film.txt", "r")

        for riga in f:
            parti = riga.strip().split(";")

            nuovo = {
                "nome": parti[0],
                "anno": int(parti[1]),
                "incasso": float(parti[2])
            }

            film.append(nuovo)

        f.close()
    except:
        print("File non trovato")


# =======================
# SALVATAGGIO JSON
# =======================
def salva_json():
    f = open("film.json", "w")
    json.dump(film, f)
    f.close()


def carica_json():
    global film
    try:
        f = open("film.json", "r")
        film = json.load(f)
        f.close()
    except:
        print("File json non trovato")


# =======================
# MENU
# =======================
carica_json()   # carica i film all'avvio

while True:

    print("\n1 Inserisci film")
    print("2 Mostra film")
    print("3 Modifica film")
    print("4 Cancella film")
    print("5 Salva con separatore")
    print("6 Salva JSON")
    print("0 Esci")

    scelta = input("Scelta: ")

    if scelta == "1":
        inserisci_film()

    elif scelta == "2":
        mostra_film()

    elif scelta == "3":
        modifica_film()

    elif scelta == "4":
        cancella_film()

    elif scelta == "5":
        salva_separatore()

    elif scelta == "6":
        salva_json()

    elif scelta == "0":
        salva_json()
        break