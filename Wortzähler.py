eingabe = input("gebe einen Text ein: ")
eingaben = eingabe.split()
gelesen = []
print("Anzahl der Wörter: " + str(len(eingaben)))
weiter = input("anzahl der einzelnen Wörter? (ja(1),nein(0))")
for i in range(len(eingaben)):
    eingaben[i] = eingaben[i].lower()
for i in range(len(eingaben)):
    eingaben[i] = eingaben[i].replace(".", "")
    eingaben[i] = eingaben[i].replace(",", "")
if weiter == "1":
    for i in range(len(eingaben)):
        wortvorhanden = 0
        anzahl = 0
        wort = eingaben[i]
        for k in range(len(gelesen)):
            if wort == gelesen[k]:
                wortvorhanden = 1
                break
        if  wortvorhanden == 0:
            for j in range(len(eingaben)):
                if wort == eingaben[j]:
                    anzahl += 1
            gelesen.append(wort)
        if anzahl != 0 :
            print(wort + ": " + str(anzahl))