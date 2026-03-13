import os
import json
import datetime
import requests
import random
#realizzare un pprogramma dotato di un menu in grado di fornire:
# - menu di scelta dei comandi
# - gestisce / CRUD le informazioni relative a 
#  una raccolta di videofiochi
#ogni videogioco dispone delle seguenti informazioni:
#-titolo
#-piattaforma
#-supporto
#-distributore
#-PEGi
#data di uscita
#prezzo
#- genere
#- online o no?
#- num di giocatori
#- nuovo usato

#-carica
#salva
#- con api trova per esmpio copertina del gioco magari anche limmagine
#- ricerca con tute le informazioni inserite
TITOLI_FAMOSI = ["The Last of Us Part I", "The Last of Us Part II", "God of War", "God of War Ragnarok", "Red Dead Redemption 2", "Cyberpunk 2077", "Assassin's Creed Odyssey", "Assassin's Creed Valhalla", "Assassin's Creed Origins", "Ghost of Tsushima", "Spider-Man", "Spider-Man Miles Morales", "Batman Arkham Knight", "Batman Arkham City", "Watch Dogs 2", "Death Stranding", "Control", "Alan Wake 2", "Elden Ring", "Dark Souls III", "Dark Souls Remastered", "Sekiro", "Bloodborne", "Witcher 3 Wild Hunt", "Witcher 2", "Baldur's Gate 3", "Divinity Original Sin 2", "Skyrim", "Fallout 4", "Fallout New Vegas", "Mass Effect Legendary Edition", "Dragon Age Inquisition", "Final Fantasy VII Remake", "Final Fantasy XVI", "Final Fantasy XV", "Persona 5 Royal", "Persona 4 Golden", "Monster Hunter World", "Monster Hunter Rise", "Xenoblade Chronicles 3", "Fire Emblem Three Houses", "Doom Eternal", "Doom 2016", "Halo Infinite", "Halo 5 Guardians", "Call of Duty Modern Warfare", "Call of Duty Warzone", "Battlefield 2042", "Battlefield V", "Titanfall 2", "Wolfenstein II", "Bioshock Infinite", "Bioshock Remastered", "Metro Exodus", "Prey", "Deathloop", "Borderlands 3", "Borderlands 2", "Destiny 2", "Overwatch 2", "Apex Legends", "Valorant", "Counter-Strike 2", "Hollow Knight", "Hades", "Celeste", "Cuphead", "Ori and the Blind Forest", "Ori and the Will of the Wisps", "Shovel Knight", "Stardew Valley", "Undertale", "Disco Elysium", "Return of the Obra Dinn", "Inside", "Limbo", "Little Nightmares", "Little Nightmares 2", "Spiritfarer", "Tunic", "Outer Wilds", "Subnautica", "No Man's Sky", "Minecraft", "Terraria", "GTA V", "GTA San Andreas", "Zelda Breath of the Wild", "Zelda Tears of the Kingdom", "Horizon Zero Dawn", "Horizon Forbidden West", "Far Cry 5", "Far Cry 6", "Just Cause 4", "Dying Light 2", "Days Gone", "Forza Horizon 5", "Forza Horizon 4", "Gran Turismo 7", "Need for Speed Heat", "F1 2023", "Mario Kart 8 Deluxe", "Rocket League", "Resident Evil 2 Remake", "Resident Evil 3 Remake", "Resident Evil Village", "Silent Hill 2 Remake", "Amnesia Rebirth", "Outlast 2", "Phasmophobia", "Civilization VI", "XCOM 2", "Into the Breach", "Crusader Kings III", "Total War Warhammer III", "Age of Empires IV", "Two Point Hospital", "Planet Zoo", "RimWorld", "Street Fighter 6", "Mortal Kombat 11", "Tekken 7", "Guilty Gear Strive", "Dragon Ball FighterZ"]
API_KEY  = "3bde93c11b9345fc9d1e484fc9043147"
BASE_URL = "https://api.rawg.io/api"
raccolta = [
    {
        "id": "D24",
        "titolo": "The Last of Us Part I",
        "piattaforma": "PS5",
        "supporto": "Disco",
        "distributore": "Sony",
        "pegi": 18,
        "data_uscita": "02-09-2022",
        "prezzo": 79.99,
        "genere": "Action Adventure",
        "online": False,
        "num_giocatori": 1,
        "condizione": "Nuovo",
        "copertina": ""
    }
]
def prendi_giochi_da_api(raccolta_presa, cicli): 
    for i, titolo in enumerate(TITOLI_FAMOSI):
        if i >= cicli:
            break
        gioco = api_to_dizionario(titolo)
        if gioco is not None:
            raccolta_presa.append(gioco)
    

def cerca_gioco_api(titolo):
    url = f"{BASE_URL}/games"
    params = {"key": API_KEY, "search": titolo, "page_size": 5}
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def api_to_dizionario(titolo):
    dati = cerca_gioco_api(titolo)
    if dati is None or not dati.get("results"):
        print(" Gioco non trovato.")
        return None
    g = dati["results"][0]
    return {
        "id"           : str(g.get("id", "N/D")),
        "titolo"       : g.get("name", "N/D"),
        "piattaforma"  : g["platforms"][0]["platform"]["name"] if g.get("platforms") else "N/D",
        "supporto"     : "Download",
        "distributore" : "N/D",
        "pegi"         : g.get("esrb_rating", {}).get("name", "N/D") if g.get("esrb_rating") else "N/D",
        "data_uscita"  : g.get("released", "N/D"),
        "prezzo"       : random.uniform(10.0, 80.0), 
        "genere"       : g["genres"][0]["name"] if g.get("genres") else "N/D",
        "online"       : False,
        "num_giocatori": 1,
        "condizione"   : random.choice(["Nuovo", "Usato","N/D"]),
        "copertina"    : g.get("background_image", "")
    }



def menu_scelta():
    print("="*40)
    print("GESTIONE COLLEZIONE VIDEOGIOCHI")
    print("="*40)
    print("1. carica tutti i giochi disponibili sul sito")
    print("2. Visualizza collezione")
    print("3. Aggiungi gioco (manuale)")
    print("4. Modifica gioco")
    print("5. Elimina gioco")
    print("0. Esci")
    scelta = input("Scegli un'opzione: ")
    return scelta



def mostra_gioco(gioco):
    print()
    print(f"  {'─'*36}")
    print(f"  {gioco.get('titolo','N/D')}  [{gioco.get('id','')}]")
    print(f"  {'─'*36}")
    print(f"  Piattaforma  : {gioco.get('piattaforma','N/D')}")
    print(f"  Supporto     : {gioco.get('supporto','N/D')}")
    print(f"  Distributore : {gioco.get('distributore','N/D')}")
    print(f"  PEGI         : {gioco.get('pegi','N/D')}")
    print(f"  Data uscita  : {gioco.get('data_uscita','N/D')}")
    print(f"  Prezzo       : {gioco.get('prezzo',0.0):.2f} €")
    print(f"  Genere       : {gioco.get('genere','N/D')}")
    print(f"  Online       : {'Sì' if gioco.get('online') else 'No'}")
    print(f"  Giocatori    : {gioco.get('num_giocatori','N/D')}")
    print(f"  Condizione   : {gioco.get('condizione','N/D')}")
    copertina = gioco.get("copertina","")
    if copertina:
        print(f"   Copertina : {copertina}")
    else:
        print(f"   Copertina : (nessuna immagine)")

def visualizza_tutti(raccolta_presa):
    if not raccolta_presa:
        print("  La collezione è vuota.")
        return
    print(f" COLLEZIONE — {len(raccolta_presa)} gioco/i")
    for gioco in raccolta_presa:
        mostra_gioco(gioco)

prendi_giochi_da_api(raccolta, 10)
visualizza_tutti(raccolta)

controllo = True
while controllo:
    scelta = menu_scelta()
    if scelta == "1":
        prendi_giochi_da_api(raccolta, 10)
        print("Giochi caricati con successo!")
    elif scelta == "2":
        visualizza_tutti(raccolta)
    elif scelta == "3":
        print("Funzione di aggiunta gioco (manuale) non ancora implementata.")
    elif scelta == "4":
        print("Funzione di modifica gioco non ancora implementata.")
    elif scelta == "5":
        print("Funzione di eliminazione gioco non ancora implementata.")
    elif scelta == "0":
        print("Uscita in corso...")
        controllo = False
    else:
        print("Scelta non valida. Riprova.")