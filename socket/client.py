import socket
import threading

nickname = input("choose a nickname ")
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect(('localhost', 40000))


def receive():
        while True:
            try:
                message = c.recv(1024).decode('ascii')
                if message == 'NICK':
                    c.send(bytes(nickname.encode('ascii')))
                elif message == 'SESSION ENDED BY THE HOST ':
                    c.close()
                    print("Your Chat has ended")
                    break
                else:
                    print(message)

            except Exception as e:
                print(f"An error {e} has occurred!")
                c.close()
                break


def write():
    try:
        while True:
            m = input()
            message = f"{nickname} : {m}"
            c.send(message.encode('ascii'))
            if m == 'END':
                try:
                    while True:
                        c.send('Left'.encode('ascii'))
                        c.close()

                except:
                    print("you left")
                    break

    except:
        print("No longer in chat ")


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
