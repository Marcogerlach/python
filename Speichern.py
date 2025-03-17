def neuspeichern(inhalt):
    with open("Strichliste.txt", "w") as file:
        file.write(inhalt)

def auslesen():
    with open("Strichliste.txt", "r") as file:
        inhalt = file.read()
    return inhalt

inhalte = auslesen().split()
lauf = True
while lauf:
    nameda = False
    namewo = 0
    mach  = input("Wollen sie speichern, oder ausgeben: (S(speichern)/A(ausgabe)/E(Exit))" )
    if mach == "S":
        name = input("Bitte Namen eingeben: ")
        for i in range(len(inhalte)):
            if name.lower() == inhalte[i].lower():
                nameda = True
                namewo = i
        if(nameda == False):
            inhalte.append(name)
            inhalte.append("I")
        else:
            inhalte[namewo + 1] += "I"
        neuspeichern(" ".join(inhalte)) 
        print("Name wurde gespeichert.")
    elif mach == "E":
        lauf = False
    elif mach == "A":
        ausname = input("Von welchem namen wollen sie die Striche ausgelesen bekommen: (A(alle))")
        if ausname == "A":
            print(auslesen())
        else:
            for i in range(len(inhalte)):
                if inhalte[i].lower() == ausname.lower():
                    print(ausname + " " + str(len(inhalte[i + 1])))
    else:
        print("Ungültige Eingabe, bitte S, A oder E(Exit) eingeben.")