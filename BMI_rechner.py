def bmiberechnung(groesse, gewicht):
    print(gewicht / (groesse ** 2))

gewicht = float(input("gebe dein Gewicht ein: "))
groesse = float(input("gebe deine Größe ein: (in metern)"))
bmiberechnung(groesse, gewicht)