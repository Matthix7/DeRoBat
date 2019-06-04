// Header pour le fichier mainSocket.cpp
// Description des fonctions présentes
// Définition structure de données


typedef struct transmission_data_sonar{
//communication de l'angle et de la profondeur
	float angle;
	float distance;
} data_sonar;


int GetFirstObstacleDist(unsigned char* scanline, unsigned char threshold, double minDist, double maxDist, 
						 int NBins, int RangeScale, double* pDist);

data_sonar exec();
