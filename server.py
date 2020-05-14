from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from person import Person

# GLOBAL VARS
HOST = "localhost"
PORT = 4400
# BUFSIZE is how big the messages can be
BUFSIZ = 512
persons = []
ADDR = (HOST, PORT)
MAX_CONNECTION = 10
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR) # sets up the server

def broadcast(msg, name):
    for person in persons:
        client = person.client
        client.send(bytes(name+": ",'utf8')+msg)


def client_communication(person):
    run = True
    client = person.client
    addr = person.addr
    #getting name
    name = client.recv((BUFSIZ).decode('utf8'))
    msg=f'{name} has joinned the chat'
    broadcast(msg)
    while run:
        msg = client.rev(BUFSIZ)
        if msg == bytes('{quit}', 'utf8'):
            broadcast(f'{name} is leaving.......', 'SYSTEM')
            client.send(bytes('{quit}', 'utf8'))
            client.close()
            persons.remove(person)
        else:
            client.send(msg, name)


def wait_for_connection(SERVER):
    run = True
    while run:
        try:
            client, addr = SERVER.accept()
            print(f'[CONNECTION] {addr} connected !')
            person = Person(addr, client)
            persons.append(person)
            Thread(target=client_communication,args=(person,)).start()
        except Exception as e:
            print('[FAILURE]',e)
            run=False
        print('SERVER CRASHED')


if __name__ == '__main__':
    SERVER.listen(MAX_CONNECTION)
    print('Waiting for connection......')
    ACCEPT_THREAD =  Thread(target=wait_for_connection, args=(SERVER,))
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()

