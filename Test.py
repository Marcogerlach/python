def ausgang(a):
    return a * 2

def beleidigen(name):
    return "Fick dich, " + name

PersonA = {"name" : "Marco","alter" : 20}

zahlen = [0]

ausgabe = 2
for i in range(5):
    zahlen.append(i + 1)

for i in range(len(zahlen)):
    print(zahlen[i])
while ausgabe > 0:
    print(beleidigen(PersonA["name"]))
    ausgabe -= 1

class Person:
    def __init__(self, name, alter, arbeitsgeber):
        self.name = name
        self.alter = alter
        self.arbeitsgeber = arbeitsgeber
    
    def vorstellen(self):
        print(f"Hallo, ich bin {self.name} und bin {self.alter} jahre alt!")

    def arbeit(self):
        print(f"Ich arbeite bei {self.arbeitsgeber}.")

p = Person("Marco", 20, "DRV Bund")
p.vorstellen()
p.arbeit()
print(beleidigen(p.name))