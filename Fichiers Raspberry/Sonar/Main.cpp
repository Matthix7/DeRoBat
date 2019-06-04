#include "MT.h"
#include "RazorAHRS.h"
#include "NMEADevice.h"
#include "ublox.h"
#include "SwarmonDevice.h"
#include "P33x.h"
#include "SSC32.h"
#include "Pololu.h"
#include "MiniSSC.h"
#include "IM483I.h"
#include "MDM.h"
#include "Hokuyo.h"
#include "RPLIDAR.h"
#include "Seanet.h"
#include "PathfinderDVL.h"
#include "mainSocket.h"
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

#define closesocket(sock) close((sock))

#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h> 
extern "C" {
#include "sock.h"
}
#define INVALID_SOCKET (-1)
#define SOCKET_ERROR (-1)

typedef int SOCKET;
typedef struct sockaddr_in SOCKADDR_IN;
typedef struct sockaddr SOCKADDR;


// Comment/uncomment lines depending on the device you wish to test.
// Change the device path and other parameters in the configuration files if necessary.
// If you are using an IDE, check that the configuration files are in the correct folder for that IDE 
// (e.g. sometimes in the generated ../Test_devices-build-desktop folder for Qt).

// min and max might cause incompatibilities on Linux...
#ifndef _MSC_VER
#ifndef max
#define max(a,b) (((a) > (b)) ? (a) : (b))
#endif // max
#ifndef min
#define min(a,b) (((a) < (b)) ? (a) : (b))
#endif // min
#endif // _MSC_VER

/*
Return the distance to the first obstacle from a sonar scanline.
The function does not check any argument.

unsigned char* scanline : (IN) Pointer to the sonar scanline to process.
unsigned char threshold : (IN) Threshold that indicates an obstacle (from 0 to 255).
double minDist : (IN) Distance from which we begin the search of the first 
obstacle (in m).
double maxDist : (IN) Distance to which we stop the search of the first 
obstacle (in m).
int NBins : (IN) Number of bins per scanline.
int RangeScale : (IN) Sonar range scale.
double* pDist : (INOUT) Valid pointer that will receive the distance to the 
first obstacle in m. Return -1 if all the bins are under the threshold (i.e. 
no obstacle).

Return : EXIT_SUCCESS or EXIT_FAILURE if there is an error.
*/
int GetFirstObstacleDist(unsigned char* scanline, unsigned char threshold, double minDist, double maxDist, 
						 int NBins, int RangeScale, double* pDist)
{
	double r0 = (double)NBins/(double)RangeScale, r1 = (double)RangeScale/(double)NBins;
	int minBin = max(0, (int)(minDist*r0)), maxBin = min(NBins-1, (int)(maxDist*r0)), i = 0;

	i = minBin;
	while ((i <= maxBin) && (scanline[i] < threshold)) i++;
	if (i > maxBin) *pDist = -1; else *pDist = (double)i*r1; // Convert in m.

	return EXIT_SUCCESS;
}

int main(void){
    	
	fd_set rdfs;
	
	/* creation of service sockets */
	SOCKET socketConnection = init_connection_server(PORTConnection);
	int max = socketConnection;
    
    FD_ZERO(&rdfs);
    FD_SET(socketConnection, &rdfs);
                    
    if(select(max + 1, &rdfs, NULL, NULL, NULL) == -1){
        perror("select()");
        exit(errno);
    }
    
    
    else if(FD_ISSET(socketConnection, &rdfs)){
			/* Un client se connecte aux services */
			printf("Patientez pendant qu'un client se connecte sur le port %d...\n", PORTConnection);
			SOCKADDR_IN csin = { 0 };
			socklen_t crecsize = sizeof(csin);
			
			//SOCKET cConnectionSock = accept(socketConnection, (SOCKADDR *)&csin, &crecsize);
			SOCKET sConnection = accept(socketConnection, (SOCKADDR *)&csin, &crecsize);
			printf("Un client se connecte avec la socket %d de %s:%d\n", sConnection, inet_ntoa(csin.sin_addr), htons(csin.sin_port));

            if(sConnection == SOCKET_ERROR){
				perror("accept()");
            }
               
                MT mt;
                MTDATA mtdata;
                RAZORAHRS razorahrs;
                RAZORAHRSDATA razorahrsdata;
                NMEADEVICE nmeadevice;
                NMEADATA nmeadata;
                UBLOX ublox;
                SWARMONDEVICE swarmondevice;
                SWARMONDATA swarmondata;
                P33X p33x;
                double value = 0;
                int ivalue = 0;
                SSC32 ssc32;
                POLOLU pololu;
                MINISSC minissc;
                IM483I im483i;
                double u1 = 0.25, u2 = -0.25;
                MDM mdm;
                char b = 0;
                int receivedbytes = 0;
                unsigned char buf[256];
                HOKUYO hokuyo;
                double angles[MAX_SLITDIVISION_HOKUYO];
                double distances[MAX_SLITDIVISION_HOKUYO];
                RPLIDAR rplidar;
                BOOL bNewScan = FALSE;
                int quality = 0;
                SEANET seanet;
                double angle = 0, d = 0;
                unsigned char scanline[MAX_NB_BYTES_SEANET];
                PATHFINDERDVL pathfinderdvl;

                // Disable buffering for printf()...
                setbuf(stdout, NULL);

            #ifdef _WIN32
                // Prevent display/system sleep...
                SetThreadExecutionState(ES_CONTINUOUS|ES_DISPLAY_REQUIRED);
                //SetThreadExecutionState(ES_CONTINUOUS|ES_SYSTEM_REQUIRED);
            #else
            #ifndef DISABLE_IGNORE_SIGPIPE
                // See https://stackoverflow.com/questions/17332646/server-dies-on-send-if-client-was-closed-with-ctrlc...
                if (signal(SIGPIPE, SIG_IGN) == SIG_ERR)
                {
                    PRINT_DEBUG_WARNING(("signal failed. \n"));
                }
            #endif // DISABLE_IGNORE_SIGPIPE
            #endif // _WIN32

                // Initialize to 0 all the fields of the structure.
                memset(&mt, 0, sizeof(MT));
                memset(&razorahrs, 0, sizeof(RAZORAHRS));
                memset(&nmeadevice, 0, sizeof(NMEADEVICE));
                memset(&ublox, 0, sizeof(UBLOX));
                memset(&swarmondevice, 0, sizeof(SWARMONDEVICE));
                memset(&p33x, 0, sizeof(P33X));
                memset(&ssc32, 0, sizeof(SSC32));
                memset(&pololu, 0, sizeof(POLOLU));
                memset(&minissc, 0, sizeof(MINISSC));
                memset(&im483i, 0, sizeof(IM483I));
                memset(&mdm, 0, sizeof(MDM));
                memset(&hokuyo, 0, sizeof(HOKUYO));
                memset(&rplidar, 0, sizeof(RPLIDAR));
                memset(&seanet, 0, sizeof(SEANET));
                memset(&pathfinderdvl, 0, sizeof(PATHFINDERDVL));
                ConnectSeanet(&seanet, "Seanet0.txt");
                FILE* fichier = NULL;
                fichier = fopen("test.txt", "w");
                for (;;)
                {
                    
                    
                    
                    // Wait a little bit...
                    mSleep(5);

                    angle = 0; // Will receive the angle of the ping in deg.
                    memset(scanline, 0, sizeof(scanline)); // Will receive the data of the ping (NBins values in [0..255]).
                    // Get a ping. Note that the sonar does not ping by default, therefore you should 
                    // request pings yourself to make the sonar ping and rotate...
                    GetHeadDataSeanet(&seanet, scanline, &angle);
                    // Simple detection of the first obstacle.
                    d = 0; // Will receive the distance in m of the first obstacle at angle.
                    GetFirstObstacleDist(scanline, 70, 0.5, seanet.RangeScale, seanet.NBins, seanet.RangeScale, &d);
                    
                    
                    
                    ////////////////////////////////////////////////////////////////////////////////////////////
                    /////////////////            Donnees a recuperer             //////////////////////////////
                    //////////////////////////////////////////////////////////////////////////////////////////
                    //printf("%f deg; %f m\n", angle, d);
                    fprintf(fichier, "%f \t %f \n", angle,d);
                    ////////////////////////////////////////////////////////////////////////////////////////////
                    /////////////////                 angle et d                 //////////////////////////////
                    //////////////////////////////////////////////////////////////////////////////////////////
                    
                    char msg_a_envoyer[BUF_SIZE];
                    sprintf(msg_a_envoyer, "(%f,%f) ", d, angle);
                    printf("%s\n", msg_a_envoyer);
                    
                    write_to_client(sConnection, msg_a_envoyer);
                    
                }
                fclose(fichier);
                DisconnectSeanet(&seanet);
        }

    sleep(2); //Attente que les fermetures clients se fassent bien, en cas de non respect de l'ordre de fermeture
	end_connection_server(socketConnection);
    printf("Fermeture du serveur terminée\n");

	
	

	return EXIT_SUCCESS;
}
