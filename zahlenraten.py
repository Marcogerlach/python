import json
import random
import time
import firebase_admin
from firebase_admin import credentials, db

# Verbindung zur Firebase-Datenbank herstellen
cred = credentials.Certificate("zahlenraetzel-firebase-adminsdk-fbsvc-3f429f03e3.json")  
firebase_admin.initialize_app(cred, {"databaseURL": "https://zahlenraetzel-default-rtdb.europe-west1.firebasedatabase.app/"})

# Referenz zur Highscore-Datenbank
ref = db.reference("highscores")

# Highscore hinzufügen
def add_highscore(name, modus, zeit):
    ref.push({"name": name, "modus1": modus, "Zeit1": zeit})
    print(f"Highscore für {name} gespeichert!")

# Highscores abrufen & sortieren
def get_highscores():
    highscores = ref.get()
    if highscores:
        sorted_scores = sorted(highscores.values(), key=lambda x: x["Zeit1"], reverse=False)
        return sorted_scores
    return []

# Test: Highscore speichern
#add_highscore("Alice","1", "300")
#add_highscore("Bob", 1500)

# Test: Highscores abrufen
#print("🏆 Highscores:")
def checknamen(name):
    for entry in get_highscores():
        if entry.get("name") == name:
            return True
    return False  

def neuspeichern(stats):
    with open("Statistik.json", "w") as file:
        json.dump(stats, file)

def namespeichern(name):
    with open("name.json", "w") as file:
        json.dump({"name": name}, file)

def namelesen():
    try:
        with open("name.json", "r") as file:
            name_data = json.load(file)
        return name_data["name"]
    except (FileNotFoundError, json.JSONDecodeError):
        return ""  


def auslesen():
    try:
        with open("Statistik.json", "r") as file:
            stats = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        stats = {"0": [], "1": [], "2": [], "z0": [], "z1" : [], "z2" : []}  
    return stats


stats = auslesen()
option = "ja"
while option.lower() == "ja":
    eingaben = []
    while True:
        if namelesen() == "":
            name = input("Geben sie einen Namen ein für die Statistik: ")
            if not checknamen(name):
                namespeichern(name)
                print("Name gespeichert!")
                break
            else:
                print("Name existiert schon!")
        else:
            break

    stat = input("Wollen sie die Statistik sehen, oder die Einstellungen öffnen? (Statistik(0)/Einstellungen(1)/nein(2)) ")
    if stat.lower() == "0":
        
        alle_werte = stats["0"]
        if alle_werte:
            durchschnitt = sum(alle_werte) / len(alle_werte)
            print("Durchschnittliche Versuche modi leicht: " + str(durchschnitt))
        else:
            print("Keine Statistik vorhanden.")
        alle_werte1 = stats["1"]
        if alle_werte1:
            durchschnitt = sum(alle_werte1) / len(alle_werte1)
            print("Durchschnittliche Versuche modi Normal: " + str(durchschnitt))
        else:
            print("Keine Statistik vorhanden.")
        alle_werte2 = stats["2"]
        if alle_werte2:
            durchschnitt = sum(alle_werte2) / len(alle_werte2)
            print("Durchschnittliche Versuche modi Schwer: " + str(durchschnitt))
        else:
            print("Keine Statistik vorhanden.")
        alle_wertez0 = stats["z0"]
        if alle_wertez0:
            durchschnitt = sum(alle_wertez0) / len(alle_wertez0)
            print(f"Durchschnittliche Zeit im Zeit modi leicht: {durchschnitt:.2f}")
        else:
            print("Keine Statistik vorhanden.")
        alle_wertez1 = stats["z1"]
        if alle_wertez1:
            durchschnitt = sum(alle_wertez1) / len(alle_wertez1)
            print(f"Durchschnittliche Zeit im Zeit modi Normal: {durchschnitt:.2f}")
        else:
            print("Keine Statistik vorhanden.")
        alle_wertez2 = stats["z2"]
        if alle_wertez2:
            durchschnitt = sum(alle_wertez2) / len(alle_wertez2)
            print(f"Durchschnittliche Zeit im Zeit modi Schwer: {durchschnitt:.2f}")
        else:
            print("Keine Statistik vorhanden.")

    obermodi = input("Zeitmodus(0)/Normal(1)")
    if obermodi == "1":
        modi = input("Willst du einen leichten Modus(0), einen normalen Modus(1), oder einen schweren Modus(2)? ")
        grenze = 0
        if modi == "0":
            zahl = random.randint(1, 50)
            grenze = 50
        elif modi == "1":
            zahl = random.randint(1, 100)
            grenze = 100
        else:
            zahl = random.randint(1, 200)
            grenze = 200
        while True:
            try:
                print(f"Deine bisherigen Eingaben sind {eingaben}")
                eingabe = int(input(f"Gebe eine Zahl zwischen 1 und {grenze} ein: "))
            except ValueError:
                print("Bitte eine gültige Zahl eingeben.")
                continue
            if eingabe > grenze:
                print(f"{eingabe} ist zu groß")
                continue
            elif eingabe < 1:
                print(f"{eingabe} ist zu klein")
                continue
            if eingabe in eingaben:
                print(f"{eingabe} hast du schon eingegeben.")
                continue

            eingaben.append(eingabe)
            if zahl == eingabe:
                print(f"{zahl} ist richtig und du hast folgende Zahlen falsch geraten: {len(eingaben) - 1}")
                stats[modi].append(len(eingaben))
                neuspeichern(stats)
                break
            elif zahl < eingabe:
                print("Die gesuchte Zahl ist kleiner.")
            elif zahl > eingabe:
                print("Die gesuchte Zahl ist größer.")
    elif obermodi == "0":
        modi = input("Willst du einen leichten Modus(0), einen normalen Modus(1), oder einen schweren Modus(2)? ")
        grenze = 0
        if modi == "0":
            zahl = random.randint(1, 50)
            grenze = 50
        elif modi == "1":
            zahl = random.randint(1, 100)
            grenze = 100
        else:
            zahl = random.randint(1, 200)
            grenze = 200
        start = time.time()
        while True:
            try:
                print(f"Deine bisherigen Eingaben sind {eingaben}")
                eingabe = int(input(f"Gebe eine Zahl zwischen 1 und {grenze} ein: "))
            except ValueError:
                print("Bitte eine gültige Zahl eingeben.")
                continue
            if eingabe > grenze:
                print(f"{eingabe} ist zu groß")
                continue
            elif eingabe < 1:
                print(f"{eingabe} ist zu klein")
                continue
            if eingabe in eingaben:
                print(f"{eingabe} hast du schon eingegeben.")
                continue

            eingaben.append(eingabe)
            if zahl == eingabe:
                end = time.time()
                zeit = end - start
                print(f"{zahl} ist richtig und du hast {len(eingaben) - 1} falsch geraten und {zeit:.2f} Sekunden gebraucht")
                stats["z" + modi].append(float(f"{zeit:.2f}"))
                neuspeichern(stats)
                break
            elif zahl < eingabe:
                print("Die gesuchte Zahl ist kleiner.")
            elif zahl > eingabe:
                print("Die gesuchte Zahl ist größer.")
    datenstat = get_highscores()
    found = False
    for entry in datenstat:
        if namelesen() == entry["name"]:
            found = True
        
            if float(entry["Zeit1"]) > zeit:
                add_highscore(namelesen(), modi, float(f"{zeit:.2f}"))
    if not found:
        add_highscore(namelesen(), modi, float(f"{zeit:.2f}"))
    option = input("Wollen sie weiter spielen: (ja(0)/nein(1))")
    if option == "1":
        print("Danke fürs Spielen!")
    elif option == "0":
        option = "ja"