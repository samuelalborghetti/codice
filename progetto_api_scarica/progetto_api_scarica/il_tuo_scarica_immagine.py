import requests
import os
import re

lista_url = [
    # ORIGINALI
    "https://pokeapi.co/api/v2/pokemon/",                      # 0
    "https://db.ygoprodeck.com/api/v7/cardinfo.php",            # 1
    "https://restcountries.com/v3.1/all?fields=name,flags,population,region",  # 2
    "https://rickandmortyapi.com/api/character",                # 3
    "https://www.themealdb.com/api/json/v1/1/search.php?s=a",   # 4
    "https://www.thecocktaildb.com/api/json/v1/1/search.php?s=a",# 5
    "https://hp-api.onrender.com/api/characters",               # 6
    "https://digi-api.com/api/v1/digimon",                      # 7
    "https://api.thecatapi.com/v1/images/search",               # 8
    "https://dog.ceo/api/breeds/image/random",                  # 9
    "https://pokeapi.co/api/v2/berry/",                         # 10

    # EXTRA (scaricabili)
    "https://randomfox.ca/floof/",                              # 11
    "https://random.dog/woof.json",                             # 12
    "https://some-random-api.com/img/dog",                      # 13 (redirect immagine)
    "https://some-random-api.com/img/cat",                      # 14 (redirect immagine)
    "https://some-random-api.com/img/birb",                     # 15 (redirect immagine)
    "https://cataas.com/cat?json=true",                         # 16 (json -> url)

    # immagini dirette (no json)
    "https://picsum.photos/800/600",                            # 17 (redirect)
    "https://placecats.com/neo/800/600",                         # 18 (immagine diretta)
    "https://placebear.com/800/600"                              # 19 (immagine diretta)
]

dizionario_immagini = []

prefissi = {
    "pokemon": "POK_",
    "yugi": "YUG_",
    "bandiera": "BAN_",
    "rickmorty": "RIC_",
    "pasto": "PAS_",
    "cocktail": "COC_",
    "harrypotter": "HAR_",
    "digimon": "DIG_",
    "gatto": "GAT_",
    "cane": "CAN_",
    "bacca": "BAC_",

    "fox": "FOX_",
    "randomdog": "RDG_",
    "dogimg": "SDG_",
    "catimg": "SCA_",
    "birbimg": "SBI_",
    "cataas": "CAT_",

    "picsum": "PIC_",
    "kitten": "KTT_",
    "bear": "BEA_"
}

def ottieni_headers(categoria=None):
    return {"User-Agent": "Mozilla/5.0"}

def nome_gia_presente(dizionario, categoria, nome):
    for j in dizionario:
        if j["categoria"] == categoria and j.get(f"nome_{categoria}") == nome:
            return True
    return False

def aggiungi(dizionario, categoria, nome, url_img):
    if not nome or not url_img or not str(url_img).startswith("http"):
        return
    if nome_gia_presente(dizionario, categoria, nome):
        return
    dizionario.append({
        "categoria": categoria,
        f"nome_{categoria}": nome,
        "link_immagine": url_img
    })

def estensione_da_content_type(content_type):
    mappa_estensioni = {
        "image/jpeg": ".jpg",
        "image/jpg": ".jpg",
        "image/png": ".png",
        "image/gif": ".gif",
        "image/webp": ".webp"
    }
    content_type = (content_type or "").split(";")[0].lower()
    return mappa_estensioni.get(content_type, ".jpg")

def scarica_immagine(elemento, cartella="immagini"):
    os.makedirs(cartella, exist_ok=True)
    categoria = elemento["categoria"]
    nome = elemento[f"nome_{categoria}"]
    url_immagine = elemento["link_immagine"]

    if not url_immagine or not str(url_immagine).startswith("http"):
        print(f"URL non valida, salto: {nome}")
        return

    prefisso = prefissi.get(categoria, categoria[0].upper() + "_")
    nome_pulito = re.sub(r'[\\/:*?"<>|]', "", str(nome))

    try:
        r = requests.get(url_immagine, headers=ottieni_headers(categoria), stream=True, timeout=20, allow_redirects=True)
    except requests.RequestException as errore:
        print(f"Errore richiesta: {nome} -> {errore}")
        return

    if r.status_code != 200:
        print(f"Errore {r.status_code}: {nome}")
        return

    content_type = (r.headers.get("content-type") or "").lower()
    if not content_type.startswith("image/"):
        print(f"Errore {r.status_code}: {nome} -> risposta non immagine ({content_type})")
        return

    estensione = estensione_da_content_type(content_type)
    nome_file = prefisso + nome_pulito + estensione
    percorso = os.path.join(cartella, nome_file)

    if os.path.exists(percorso):
        print(f"Già presente: {percorso}")
        return

    with open(percorso, "wb") as f:
        for chunk in r.iter_content(1024 * 64):
            if chunk:
                f.write(chunk)
    print(f"Salvata: {percorso}")

def get_json_sicuro(url, categoria=None):
    try:
        r = requests.get(url, headers=ottieni_headers(categoria), timeout=20, allow_redirects=True)
    except requests.RequestException:
        return None
    if r.status_code != 200:
        return None
    try:
        return r.json()
    except ValueError:
        return None

# ------------------------------
# FUNZIONI RECUPERO (stesso stile)
# ------------------------------

def trova_immagine_pokemon(url, nome):
    cerca = get_json_sicuro(url + nome, "pokemon")
    if not cerca:
        return None
    return cerca["sprites"]["front_default"]

def recupera_pokemon(url, categoria, dizionario, limite=10):
    cerca = get_json_sicuro(url + f"?limit={limite}", categoria)
    if not cerca:
        return
    for i in cerca["results"]:
        url_img = trova_immagine_pokemon(lista_url[0], i["name"])
        aggiungi(dizionario, categoria, i["name"], url_img)

def recupera_carte_yughi(url, categoria, dizionario, limite=10):
    cerca = get_json_sicuro(url, categoria)
    if not cerca:
        return
    for n in cerca["data"][:limite]:
        url_img = n["card_images"][0]["image_url"]
        aggiungi(dizionario, categoria, n["name"], url_img)

def recupera_bandiere(url, categoria, dizionario, limite=10):
    cerca = get_json_sicuro(url, categoria)
    if not cerca:
        return
    for n in cerca[:limite]:
        nome = n["name"]["common"]
        url_img = n["flags"]["png"]
        aggiungi(dizionario, categoria, nome, url_img)

def recupera_rick_e_morty(url, categoria, dizionario, limite=10):
    cerca = get_json_sicuro(url + "?page=1", categoria)
    if not cerca:
        return
    for n in cerca["results"][:limite]:
        aggiungi(dizionario, categoria, n["name"], n["image"])

def recupera_pasti(url, categoria, dizionario, limite=10):
    cerca = get_json_sicuro(url, categoria)
    if not cerca or not cerca.get("meals"):
        return
    for n in cerca["meals"][:limite]:
        aggiungi(dizionario, categoria, n["strMeal"], n["strMealThumb"])

def recupera_cocktail(url, categoria, dizionario, limite=10):
    cerca = get_json_sicuro(url, categoria)
    if not cerca or not cerca.get("drinks"):
        return
    for n in cerca["drinks"][:limite]:
        aggiungi(dizionario, categoria, n["strDrink"], n["strDrinkThumb"])

def recupera_harry_potter(url, categoria, dizionario, limite=10):
    cerca = get_json_sicuro(url, categoria)
    if not cerca:
        return
    for n in cerca[:limite]:
        if n.get("image"):
            aggiungi(dizionario, categoria, n["name"], n["image"])

def recupera_digimon(url, categoria, dizionario, limite=10):
    cerca = get_json_sicuro(url + f"?pageSize={limite}", categoria)
    if not cerca:
        return
    for n in cerca["content"][:limite]:
        aggiungi(dizionario, categoria, n["name"], n["image"])

def recupera_gatti(url, categoria, dizionario, limite=10):
    cerca = get_json_sicuro(url + f"?limit={limite}", categoria)
    if not cerca:
        return
    for n in cerca:
        aggiungi(dizionario, categoria, n["id"], n["url"])

def recupera_cani(url, categoria, dizionario, limite=10):
    for i in range(limite):
        cerca = get_json_sicuro(url, categoria)
        if not cerca:
            continue
        url_img = cerca.get("message")
        nome = f"cane_{i+1}"
        aggiungi(dizionario, categoria, nome, url_img)

def recupera_bacche_pokemon(url, categoria, dizionario, limite=10):
    cerca = get_json_sicuro(url + f"?limit={limite}", categoria)
    if not cerca:
        return
    for i in cerca["results"]:
        dettaglio = get_json_sicuro(i["url"], categoria)
        if not dettaglio:
            continue
        item = get_json_sicuro(dettaglio["item"]["url"], categoria)
        if not item:
            continue
        url_img = item["sprites"]["default"]
        aggiungi(dizionario, categoria, i["name"], url_img)

# EXTRA

def recupera_randomfox(url, categoria, dizionario, limite=10):
    nomi_esistenti = []
    for j in dizionario:
        if j["categoria"] == categoria:
            nomi_esistenti.append(j[f"nome_{categoria}"])

    presi = 0
    tentativi = 0
    while presi < limite and tentativi < limite * 20:
        tentativi += 1
        try:
            r = requests.get(url, headers=ottieni_headers(categoria), timeout=20)
        except requests.RequestException:
            continue

        if r.status_code != 200:
            continue
        try:
            cerca = r.json()
        except ValueError:
            continue

        url_img = cerca.get("image")
        nome = f"fox_{presi+1}"

        if nome not in nomi_esistenti and url_img and url_img.startswith("http"):
            dizionario.append({
                "categoria": categoria,
                f"nome_{categoria}": nome,
                "link_immagine": url_img
            })
            presi += 1
def recupera_some_random_api_json(url, categoria, dizionario, limite=10):
    nomi_esistenti = []
    for j in dizionario:
        if j["categoria"] == categoria:
            nomi_esistenti.append(j[f"nome_{categoria}"])

    presi = 0
    tentativi = 0
    while presi < limite and tentativi < limite * 20:
        tentativi += 1
        try:
            r = requests.get(url, headers=ottieni_headers(categoria), timeout=20)
        except requests.RequestException:
            continue

        if r.status_code != 200:
            continue

        try:
            cerca = r.json()
        except ValueError:
            continue

        url_img = cerca.get("link")  # <- QUESTO è il link dell'immagine
        nome = f"{categoria}_{presi+1}"

        if nome not in nomi_esistenti and url_img and url_img.startswith("http"):
            dizionario.append({
                "categoria": categoria,
                f"nome_{categoria}": nome,
                "link_immagine": url_img
            })
            presi += 1
def recupera_randomdog(url, categoria, dizionario, limite=10):
    presi = 0
    tentativi = 0
    while presi < limite and tentativi < limite * 10:
        tentativi += 1
        cerca = get_json_sicuro(url, categoria)
        if not cerca:
            continue
        url_img = cerca.get("url")
        est = os.path.splitext((url_img or "").split("?")[0])[1].lower()
        if est in {".mp4", ".webm"}:
            continue
        nome = f"randomdog_{presi+1}"
        aggiungi(dizionario, categoria, nome, url_img)
        presi += 1

def recupera_redirect_img(url, categoria, dizionario, limite=10):
    for i in range(limite):
        try:
            r = requests.get(url, headers=ottieni_headers(categoria), allow_redirects=True, timeout=20)
        except requests.RequestException:
            continue
        url_img = r.url
        nome = f"{categoria}_{i+1}"
        aggiungi(dizionario, categoria, nome, url_img)

def recupera_cataas(url, categoria, dizionario, limite=10):
    presi = 0
    tentativi = 0
    while presi < limite and tentativi < limite * 10:
        tentativi += 1
        cerca = get_json_sicuro(url, categoria)
        if not cerca:
            continue
        identificativo = cerca.get("id") or cerca.get("_id")
        url_img = cerca.get("url")
        if not url_img and identificativo:
            url_img = f"https://cataas.com/cat/{identificativo}"
        nome = f"cataas_{identificativo}" if identificativo else f"cataas_{presi+1}"
        if nome_gia_presente(dizionario, categoria, nome):
            continue
        aggiungi(dizionario, categoria, nome, url_img)
        presi += 1

# ------------------------------
# MENU
# ------------------------------

def leggi_intero(messaggio, default=10, minimo=1, massimo=500):
    valore = input(messaggio).strip()
    if valore == "":
        return default
    try:
        n = int(valore)
        if n < minimo:
            n = minimo
        if n > massimo:
            n = massimo
        return n
    except ValueError:
        return default

def leggi_scelte(messaggio):
    testo = input(messaggio).strip()
    if testo == "":
        return []
    pezzi = testo.split(",")
    scelte = []
    for p in pezzi:
        p = p.strip()
        if p.isdigit():
            scelte.append(int(p))
    return scelte

def menu():
    print("\n=== MENU DOWNLOAD IMMAGINI ===")
    print("Scrivi i numeri delle categorie separati da virgola (es: 1,3,9)")
    print("Premi INVIO per scaricare tutto.")
    print("")
    print(" 1) Pokemon")
    print(" 2) Carte Yu-Gi-Oh")
    print(" 3) Bandiere")
    print(" 4) Rick and Morty")
    print(" 5) Pasti (MealDB)")
    print(" 6) Cocktail (CocktailDB)")
    print(" 7) Harry Potter")
    print(" 8) Digimon")
    print(" 9) Gatti (TheCatAPI)")
    print("10) Cani (Dog CEO)")
    print("11) Bacche Pokemon")
    print("12) Volpi (RandomFox)")
    print("13) RandomDog (solo immagini)")
    print("14) SomeRandomAPI Dog (redirect)")
    print("15) SomeRandomAPI Cat (redirect)")
    print("16) SomeRandomAPI Birb (redirect)")
    print("17) Cataas (cat)")
    print("18) Picsum (random)")
    print("19) PlaceCats (immagine diretta)")
    print("20) PlaceBear (immagine diretta)")
    print("")

    scelte = leggi_scelte("Scelta categorie (INVIO=tutte): ")
    limite = leggi_intero("Quante immagini per categoria? (default 10): ", default=10, minimo=1, massimo=2000)
    print("")
    return scelte, limite

def esegui_scelta(numero, limite):
    if numero == 1:
        recupera_pokemon(lista_url[0], "pokemon", dizionario_immagini, limite)
    elif numero == 2:
        recupera_carte_yughi(lista_url[1], "yugi", dizionario_immagini, limite)
    elif numero == 3:
        recupera_bandiere(lista_url[2], "bandiera", dizionario_immagini, limite)
    elif numero == 4:
        recupera_rick_e_morty(lista_url[3], "rickmorty", dizionario_immagini, limite)
    elif numero == 5:
        recupera_pasti(lista_url[4], "pasto", dizionario_immagini, limite)
    elif numero == 6:
        recupera_cocktail(lista_url[5], "cocktail", dizionario_immagini, limite)
    elif numero == 7:
        recupera_harry_potter(lista_url[6], "harrypotter", dizionario_immagini, limite)
    elif numero == 8:
        recupera_digimon(lista_url[7], "digimon", dizionario_immagini, limite)
    elif numero == 9:
        recupera_gatti(lista_url[8], "gatto", dizionario_immagini, limite)
    elif numero == 10:
        recupera_cani(lista_url[9], "cane", dizionario_immagini, limite)
    elif numero == 11:
        recupera_bacche_pokemon(lista_url[10], "bacca", dizionario_immagini, limite)
    elif numero == 12:
        recupera_randomfox(lista_url[11], "fox", dizionario_immagini, limite)
    elif numero == 13:
        recupera_randomdog(lista_url[12], "randomdog", dizionario_immagini, limite)
    elif numero == 14:
        recupera_some_random_api_json(lista_url[13], "dogimg", dizionario_immagini, limite)
    elif numero == 15:
        recupera_some_random_api_json(lista_url[14], "catimg", dizionario_immagini, limite)
    elif numero == 16:
        recupera_some_random_api_json(lista_url[15], "birbimg", dizionario_immagini, limite)
    elif numero == 17:
        recupera_cataas(lista_url[16], "cataas", dizionario_immagini, limite)
    elif numero == 18:
        recupera_redirect_img(lista_url[17], "picsum", dizionario_immagini, limite)
    elif numero == 19:
        recupera_redirect_img(lista_url[18], "kitten", dizionario_immagini, limite)
    elif numero == 20:
        recupera_redirect_img(lista_url[19], "bear", dizionario_immagini, limite)

# ------------------------------
# MAIN
# ------------------------------

scelte, limite = menu()

if not scelte:
    scelte = list(range(1, 21))

for n in scelte:
    esegui_scelta(n, limite)

for elemento in dizionario_immagini:
    scarica_immagine(elemento)