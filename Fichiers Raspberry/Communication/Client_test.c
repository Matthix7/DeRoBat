#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <sys/time.h>
#include <string.h>
#include <math.h>
#include <semaphore.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <strings.h>
#include <errno.h>
#include <netdb.h>
#include <signal.h>
#include <unistd.h>
#include <arpa/inet.h>
#include "sock.h"





int main(int argc, char **argv)
{
	if(argc == 1)
    {
      printf("Usage : %s [address] \n", argv[0]);
      return EXIT_FAILURE;
    }
    
    char buffer[BUF_SIZE];
	char* address = argv[1];  
	
	fd_set rdfs;
	
    SOCKET socketConnection = init_connection_client(address, PORTConnection);
    int max = socketConnection;
    while(1){
    
		FD_ZERO(&rdfs);

		/* add the socket */
		FD_SET(socketConnection, &rdfs);

		if(select(max + 1, &rdfs, NULL, NULL, NULL) == -1){
			perror("select()");
			exit(errno);
		}
		if(FD_ISSET(socketConnection, &rdfs)){
			/*Le serveur donne l'ID*/
			int n = read_from_server(socketConnection, buffer);
			//  server down 
			if(n == 0){printf("Server disconnected !\n");break;}
			char* exitCondition = "Quit";  //Si serveur déconnecté, il envoit "Quit"
			if (strcmp(exitCondition, buffer)==0){break;}
			else{puts(buffer);}
			
		}	
		
	}
    end_connection_client(socketConnection);
    
    return EXIT_SUCCESS;
}
