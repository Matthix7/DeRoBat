----------- ReadMe Camera -------------
#1
Ce programme ne marqhe que pour une caméra (suffisant pour le workshop)

#2
Pour lancer le programme il faut d'abord lancer la fonction init().
Ensuite dans un boucle mettre la fonction run(cap1, DIM, K, D) pour avoir la postion en direct (sans passer par un fichier), lancer la fonction runTXT(cap1, DIM, K, D, file) pour ecrire dans le fichier file.

#3
Voir le if __name__ == "__main__": pour un exemple de fonctionnement nominale