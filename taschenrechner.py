eingabe = input("Gebe die rechnung ein, mit leerzeichen (einzel)")
eingaben = eingabe.split()
for i in range(len(eingaben)):
    if eingaben[i] == "-":
        ergebnis = float(eingaben[0]) - float(eingaben[2])
        if ergebnis.is_integer():
            print(int(ergebnis))
        else:
            print(ergebnis)
        break
    elif eingaben[i] == "+":
        ergebnis = float(eingaben[0]) + float(eingaben[2])
        if ergebnis.is_integer():
            print(int(ergebnis))
        else:
            print(ergebnis)
        break
    elif eingaben[i] == "*":
        ergebnis = float(eingaben[0]) * float(eingaben[2])
        if ergebnis.is_integer():
            print(int(ergebnis))
        else:
            print(ergebnis)
        break
    elif eingabe[i] == "/":
        ergebnis = float(eingaben[0]) / float(eingaben[2])
        if ergebnis.is_integer():
            print(int(ergebnis))
        else:
            print(ergebnis)
        break

