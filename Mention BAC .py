moyenne=float(input("Entre ta moyenne au BAC "))

i = int(0)

while i < 10 :
    print(i)
    i = i + 1


langages = ['Python', 'Javascript', 'C', 'Marius']
for l in langages:
  print(l)


if moyenne < 0 or moyenne > 20:
    print("Moyenne anormale !!!")
elif moyenne >= 10 and moyenne < 12:
    print("Assez bien")
elif moyenne >= 12 and moyenne < 14:
    print("Bien")
elif moyenne >= 14 and moyenne < 18:
    print("Très bien")
elif moyenne >= 18:
    print("Les felicitations du jury")
else:
    print("Pas de mention")
    
  