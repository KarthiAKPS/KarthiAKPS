import socket
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 40000))
s.listen()
print('Waiting for connections...')

clients = []
nicknames = []


def broadcast(message):
    for c in clients:
        c.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)

            if message == 'Left':
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                nicknames.remove(nickname)
                print(f"{nickname} left the chat ")
                broadcast(f"{nickname} left the chat".encode('ascii'))

        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            broadcast(f"{nickname} left the chat".encode('ascii'))
            break


def receive():
    while True:
        c, addr = s.accept()
        print('Connected with', str(addr))
        c.send('NICK'.encode('ascii'))
        nickname = c.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(c)
        print(f"Nickname of the client is P{nickname} ")
        broadcast(f"{nickname} joined the chat ".encode('ascii'))
        c.send('Connected to the server! Enter "END" to leave'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(c,))
        thread.start()
        kick()


def kick():
    name = input("Enter if you want to kick someone! or end - KICK/END : ").lower()
    if name == 'kick':
        n = input("Enter the person you want to kick : ")
        if n in nicknames:
            i = nicknames.index(n)
            to_close = clients[i]
            to_close.send('SESSION ENDED BY THE HOST '.encode('ascii'))
            print(f"{n} was kicked!")
            broadcast(f"{n} was kicked!".encode('ascii'))
            to_close.close()
            kick()

        else:
            print(f"{n} was not in the chat ")
            kick()
    elif name == 'end':
        end()
    else:
        print('try again')
        kick()


def end():
    broadcast("Chat has ended".encode('ascii'))
    print("Ended the chat")
    s.close()
    for i in clients:
        i.close()
    exit(0)


receive()
