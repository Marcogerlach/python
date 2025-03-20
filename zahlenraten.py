import random

def neuspeichern(inhalt):
    with open("Statistik.txt", "w") as file:
        file.write(inhalt)

def auslesen():
    with open("Statistik.txt", "r") as file:
        inhalt = file.read()
    return inhalt
inhalt = auslesen().split(" ")
option = "ja"
while option.lower() == "ja":
    eingaben = []
    zahl = random.randint(1, 100)
    stat = input("Wollen sie die statistik sehen? (ja/nein)")
    if stat == "ja":
        ins = 0
        durchschnitt = 0
        for i in range(len(inhalt)):
            if inhalt[i].isdigit():
                ins += int(inhalt[i])
        if inhalt:
            durchschnitt = float(ins) / float(len(inhalt))
        print("durschnittliche Versuche: " + str(durchschnitt))
    
    modi = input("Willst du einen leichten Modus(0), einen Normalen Modus(1), oder einen Schweren Modus(2)")
    while modi == 0:
        try:
            print(f"Deine bisherigen eingaben sind {eingaben}")
            eingabe = int(input("Gebe eine Zahl zwischen 1 und 50 ein: "))
        except ValueError:
            print("Bitte eine gültige Zahl eingeben.")
            continue
        if eingabe > 50:
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
            #statistik = len(eingaben)
            #inhalt.append(" " + str(statistik))
            #neuspeichern(" ".join(inhalt))
            break
        elif zahl < eingabe:
            print("Die gesuchte Zahl ist kleiner.")
        elif zahl > eingabe:
            print("Die gesuchte Zahl ist größer.")
    option = input("Willst du noch eine Runde spielen? (ja/nein)")
    if option.lower() == "nein":
        print("Danke fürs Spielen!")
    eingaben = []
    while modi == 1:
        try:
            print(f"Deine bisherigen eingaben sind {eingaben}")
            eingabe = int(input("Gebe eine Zahl zwischen 1 und 100 ein: "))
        except ValueError:
            print("Bitte eine gültige Zahl eingeben.")
            continue
        if eingabe > 100:
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
            statistik = len(eingaben)
            inhalt.append(" " + str(statistik))
            neuspeichern(" ".join(inhalt))
            break
        elif zahl < eingabe:
            print("Die gesuchte Zahl ist kleiner.")
        elif zahl > eingabe:
            print("Die gesuchte Zahl ist größer.")
    option = input("Willst du noch eine Runde spielen? (ja/nein)")
    if option.lower() == "nein":
        print("Danke fürs Spielen!")
    eingaben = []

    while modi == 2:
        try:
            print(f"Deine bisherigen eingaben sind {eingaben}")
            eingabe = int(input("Gebe eine Zahl zwischen 1 und 200 ein: "))
        except ValueError:
            print("Bitte eine gültige Zahl eingeben.")
            continue
        if eingabe > 200:
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
            #statistik = len(eingaben)
            #inhalt.append(" " + str(statistik))
            #neuspeichern(" ".join(inhalt))
            break
        elif zahl < eingabe:
            print("Die gesuchte Zahl ist kleiner.")
        elif zahl > eingabe:
            print("Die gesuchte Zahl ist größer.")
    option = input("Willst du noch eine Runde spielen? (ja/nein)")
    if option.lower() == "nein":
        print("Danke fürs Spielen!")
    eingaben = []

