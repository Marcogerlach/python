import random

word_list = [
    "python", "programming", "hangman", "challenge", "notebook", 
    "computer", "keyboard", "mouse", "monitor", "internet", 
    "software", "hardware", "algorithm", "function", "variable", 
    "loop", "condition", "array", "dictionary", "string", 
    "integer", "float", "boolean", "exception", "module"
]
wort = random.choice(word_list)
ausgabe = "_" * len(wort)  
antworten = []
fehler = 0
print(ausgabe)
while True: 
    antwort = input("Gebe einen Buchstaben ein: (klein)")
    antworten.append(antwort)
    buchstabe = 0
    for i in range(len(wort)):
        if wort[i] == antwort:
            buchstabe = 1
            break
    if buchstabe == 1:
        ausgabe = ""
        for i in range(len(wort)):
            if wort[i] in antworten:
                ausgabe += wort[i]
            else:
                ausgabe += "_"
    else:
        fehler += 1
    print(ausgabe)
    print(str(fehler) + " von " + "6")
    if fehler == 6:
        print("Verloren")
        break
    if ausgabe == wort:
        print("Sie haben das wort gefunden: " + wort)
        break
