# DeRoBat
Programmes permettant de faire fonctionner le démonstrateur de robot bathymétrique pour l'exposition MerXXL 2019.  



## Lancement du système
1) Allumer le circuit du bateau (switch principal, au-desssus du pont). Des LEDs doivent s'allumer sur la Raspberry.  
2) Attendre jusqu'à l'apparition du réseau Wifi raspi-DeRoBat. (environ 2 min)  
3) S'y connecter (MdP: ENSTA_MerXXL)
4) Lancer l'exécution du programme `Server.py` sur une session du PC distant.
5) Se connecter via bureau à distance (conseillé) ou ssh à la Raspberry.   
adresse IP: 10.3.141.1  
user: pi  
Mot de Passe: derobat  
6) Une fois connecté à une session de la Raspberry, ouvrir un terminal dans /Documents/DeRoBat/Sonar et un autre dans /Documents/DeRoBat/Communication.
7) Dans le terminal Sonar, lancer le programme testDevices (`./testDevices`).
8) Dans le terminal Communication, lancer le programme Client (`python3 Client.py`). Ne pas oublier le *python3*.
9) Le système est lancé. Attendre que le sonar commence ses acquisitions pour pouvoir interagir avec la fenêtre d'affichage 3D. Tous les relevés du sonar sont disponibles dans le fichier `mesures.txt`, réécrit à chaque mission.  

## Eteindre le système
1) Se placer dans la fenêtre "Webcam" d'acquisition vidéo.
2) Appuyer sur `echap`.
3) Tous les programmes devraient s'éteindre automatiquement. Si ce n'est pas le cas, `CTRL+C`...
