lang = int(input("Die wie viel ersten Fibonacci Zahlen sollen ausgegeben werden: "))
zahlen = [0, 1]
print(0)
print(1)
for i in range(2, lang):
    zahlen.append(zahlen[i - 1] + zahlen[i - 2])
    print(zahlen[i - 1] + zahlen[i - 2]) 