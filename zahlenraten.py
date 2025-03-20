import json
import random



def neuspeichern(stats):
    with open("Statistik.txt", "w") as file:
        json.dump(stats, file)

def auslesen():
    try:
        with open("Statistik.txt", "r") as file:
            stats = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        stats = {"0": [], "1": [], "2": []}  
    return stats


stats = auslesen()
option = "ja"
while option.lower() == "ja":
    eingaben = []
    stat = input("Wollen sie die Statistik sehen? (ja/nein) ")
    if stat.lower() == "ja":
        
        alle_werte = stats["0"] + stats["1"] + stats["2"]
        if alle_werte:
            durchschnitt = sum(alle_werte) / len(alle_werte)
            print("Durchschnittliche Versuche: " + str(durchschnitt))
        else:
            print("Keine Statistik vorhanden.")
    
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