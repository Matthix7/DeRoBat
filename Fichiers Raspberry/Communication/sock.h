/// Code Socket, regroupe toutes les structures et fonctions        ///
/// nécessaires pour la communication par sockets.                  ///

#ifndef SOCK_H
#define SOCK_H
#include "sock.c"
////////////////////////////////////////////////////////////////////////
///////////      Paramètres communication côté serveur     /////////////
////////////////////////////////////////////////////////////////////////


typedef int SOCKET;
typedef struct sockaddr_in SOCKADDR_IN;
typedef struct sockaddr SOCKADDR;
typedef struct in_addr IN_ADDR;

#define PORTConnection  12802
#define BUF_SIZE	1024


int init_connection_server(int port);
void end_connection_server(SOCKET sock);
void write_to_client(SOCKET sock, const char *buffer);


////////////////////////////////////////////////////////////////////////
///////////      Paramètres communication côté client      /////////////
////////////////////////////////////////////////////////////////////////


int init_connection_client(const char *address, int port);
void end_connection_client(int sock);
int read_from_server(SOCKET sock, char *buffer);

















#endif
