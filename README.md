# DeRoBat
Programmes permettant de faire fonctionner le démonstrateur de robot bathymétrique pour l'exposition MerXXL 2019.  



## Lancement du système
1) Allumer le circuit du bateau (switch principal, au-desssus du pont). Des LEDs doivent s'allumer sur la Raspberry.  
2) Attendre jusqu'à l'apparition du réseau Wifi raspi-DeRoBat. (environ 2 min)  
3) S'y connecter (MdP: ENSTA_MerXXL)
4) Lancement du programme: (2 choix possibles)
	4.0) Choix 1:
	4.1) Lancer l'exécution du programme `Server.py` sur une session du PC distant.
	4.2) Se connecter via bureau à distance (conseillé) ou ssh à la Raspberry.   
	adresse IP: 10.3.141.1  
	user: pi  
	Mot de Passe: derobat  
	4.3) Une fois connecté à une session de la Raspberry, ouvrir un terminal dans /Documents/DeRoBat/Sonar et un autre dans /Documents/DeRoBat/Communication.
	4.4) Dans le terminal Sonar, lancer le programme testDevices (`./testDevices`).
	4.5) Dans le terminal Communication, lancer le programme Client (`python3 Client.py`). Ne pas oublier le *python3*.

	4.0) Choix 2: (conseillé car utilisatiçn du flux wifi reduit, utile pour les endroits "charger" en reseau wifi (Exposition....))
	4.1) Lancer l'exécution du programme `Server.py` sur une session du PC distant.
	4.2) Se connecter en ssh à la Raspberry.   
	adresse IP: 10.3.141.1  
	user: pi  
	Mot de Passe: derobat  
	4.3) Une fois connecté à une session de la Raspberry, lancer le bash lauch.sh avec la commande nohup: nohup ~/launch.sh

9) Le système est lancé. Attendre que le sonar commence ses acquisitions pour pouvoir interagir avec la fenêtre d'affichage 3D. Tous les relevés du sonar sont disponibles dans le fichier `mesures.txt`, réécrit à chaque mission.  

## Eteindre le système
1) Se placer dans la fenêtre "Webcam" d'acquisition vidéo.
2) Appuyer sur `echap`.
3.0) Tous les programmes devraient s'éteindre automatiquement. Si ce n'est pas le cas:
3.1) Choix 1 en 4.0 : `CTRL+C`...
3.2) Choix 2 en 4.0 : Fermer Server.py (CTRL+C) puis dans le terminal connecté à la raspbery faire sudo killall ./Test_devices python3


## En fonctionnement
Sur la chaîne YouTube de notre professeur de Robotique: https://www.youtube.com/watch?v=PU-aVa9GJ1c
![alt text](https://github.com/Matthix7/DeRoBat/blob/master/Visuels/Bateau/Fischkutter/Screenshot_20190703-202959.png "En fonctionnement")
