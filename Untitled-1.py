mot_de_passe = input("Entrez votre mot de passe ")  

if len(mot_de_passe) < 6:
    print("Le mot de passe est trop court")
elif mot_de_passe == '123456':
     print("Vous ête en cours de connexion")
     mot_de_passe = mot_de_passe * 4
     print(mot_de_passe)
else:!
     print("Votre mot de passe n'est pas bon !!")

print("Le programme est terminé !!")