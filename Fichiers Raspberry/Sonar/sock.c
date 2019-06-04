///  Code Socket, regroupe toutes les structures et fonctions        ///
///  nécessaires pour la communication par sockets.                  ///
///////////////      Schémas de sockets inspirés de        /////////////
////////////    http://sdz.tdct.org/sdz/les-sockets.html     ///////////


#include "sock.h"


#define INVALID_SOCKET (-1)
#define SOCKET_ERROR (-1)

typedef int SOCKET;
typedef struct sockaddr_in SOCKADDR_IN;
typedef struct sockaddr SOCKADDR;
typedef struct in_addr IN_ADDR;
#define BUF_SIZE	1024


////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
/////////////////////     CÔTE SERVEUR     /////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////




///////////////////     Initialisation de la connection     ////////////
////////////////////////////////////////////////////////////////////////

int init_connection_server(int port){
	
	/* Socket et contexte d'adressage du serveur */
	SOCKADDR_IN sin;
	SOCKET sock;
	socklen_t recsize = sizeof(sin);

	int sock_err;

	/* Création d'une socket */
	sock = socket(AF_INET, SOCK_STREAM, 0);

	/* Si la socket est invalide */
	if(sock == INVALID_SOCKET){
		perror("socket");
		exit(errno);
	}

	/* Configuration */
	sin.sin_addr.s_addr = htonl(INADDR_ANY);
	sin.sin_port = htons(port);
	sin.sin_family = AF_INET;
	sock_err = bind(sock, (SOCKADDR*)&sin, recsize);

	/* Si la socket ne fonctionne pas */
	if(sock_err == SOCKET_ERROR)
	{
	  perror("bind()");
	  exit(errno);
	}

	/* Démarrage du listage (mode server) */
	sock_err = listen(sock, 5);
	printf("Listage du port %d...\n", port);

	/* Si la socket ne fonctionne pas */
	if(sock_err == SOCKET_ERROR)
	{
		perror("listen()");
		exit(errno);
	}

	return sock;
}


///////////////////          Fin de la connection           ////////////
////////////////////////////////////////////////////////////////////////

void end_connection_server(SOCKET sock)
{
	printf("Fermeture de la socket serveur\n");
	closesocket(sock);
}





///////////////////      Envoi d'un message au client       ////////////
////////////////////////////////////////////////////////////////////////

void write_to_client(SOCKET sock, const char *buffer)
{
	
	if(send(sock, buffer, strlen(buffer), 0) < 0)
	{
		perror("send()");
		exit(errno);
	}
}





////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
/////////////////////      CÔTE CLIENT     /////////////////////////////
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////



///////////////////     Initialisation de la connection     ////////////
////////////////////////////////////////////////////////////////////////

SOCKET init_connection_client(const char *address, int port)
{
	/* Création de la socket */
	SOCKET sock = socket(AF_INET, SOCK_STREAM, 0);
	SOCKADDR_IN sin = { 0 };
	struct hostent *hostinfo;

	if(sock == INVALID_SOCKET)
	{
		perror("socket()");
		exit(errno);
	}

	hostinfo = gethostbyname(address);
	if (hostinfo == NULL)
	{
		fprintf (stderr, "Unknown host %s.\n", address);
		exit(EXIT_FAILURE);
	}
   
	/* Configuration de la connexion */
	sin.sin_addr = *(IN_ADDR *) hostinfo->h_addr;
	sin.sin_port = htons(port);
	sin.sin_family = AF_INET;
	
	/* Si le client n'arrive pas à se connecter */
	if(connect(sock,(SOCKADDR *) &sin, sizeof(sin)) == SOCKET_ERROR)
	{
		perror("Impossible de se connecter\n");
		exit(errno);
	}
	
	printf("Connexion à %s sur le port %d\n", inet_ntoa(sin.sin_addr), htons(sin.sin_port));
	return sock;
}



///////////////////          Fin de la connection           ////////////
////////////////////////////////////////////////////////////////////////

void end_connection_client(SOCKET sock)
{
   printf("Fin de communication\n");
   closesocket(sock);
}


///////////////////       Réception données serveur         ////////////
////////////////////////////////////////////////////////////////////////

int read_from_server(SOCKET sock, char *buffer)
{
   int n = 0;

   if((n = recv(sock, buffer, BUF_SIZE - 1, 0)) < 0)
   {
      perror("recv()");
      exit(errno);
   }

   buffer[n] = 0;

   return n;
}

