import socket as so
from multiprocessing import Process, Event
from time import sleep

class Client:

    def __init__(self, client_socket, client_list, username):
        self.client_socket = client_socket
        self.client_list = client_list
        self.username = username

    def forward(self, event):
        
        while True:

            message = f"{self.username} : {self.client_socket.recv(1024).decode()}"
            
            if(event.is_set()):
                event.clear()
                break

            print(f"Message received : \n{message}")

            print(self.client_list)

            for client in self.client_list:

                if(client == self.client_socket):
                    continue
                
                client.send(message.encode())
                print("Message forwarded.")

    
def connect_clients():

    server_socket = so.socket()

    print()
    # ip_address = input("Enter IP Address : ")
    ip_address = "localhost"
    port = 9999

    server_socket.bind((ip_address, port))
    server_socket.listen(10)

    event_dict = {}
    clients = []
    client_list = []

    while True:
        
        client_socket, client_address = server_socket.accept()
        username = client_socket.recv(1024).decode()

        event_dict[username] = Event()
        print(event_dict)
        print("Event object successfully added to event_dict.")

        client_list.append(client_socket)
        print("Client socket added to client_list.")
        
        for client in clients:
            client[1] = client_list

        print("Client_list updated for each client.")

        clients.append([client_socket, client_list, username])

        print("New client added to clients.")

        if(len(client_list) > 1):
            
            for username1, event_obj1 in event_dict.items():

                if(username1 != username):
                    event_obj1.set()

            client_socket.send("Wait for Sync...".encode())

            for client in client_list:

                if(client != client_socket):
                    client.send("Someone wants to get in! Enter any letter to Sync... : ".encode())
 

            print("Waiting...")
            
            
            while(True):
                
                flag = False

                for username2, event_obj2 in event_dict.items():

                    flag = flag or event_obj2.is_set()

                    print(username2, ":", event_obj2.is_set())
                    sleep(1)

                if(not flag):
                    break

            print("Continuing...")

         

        for client in clients:

            Client_obj = Client(client[0], client[1], client[2])                      #Client(client_socket, client_list, username)
            Client_obj_method_caller_process = Process(target = Client_obj.forward, args = (event_dict[client[2]],))
            Client_obj_method_caller_process.start()

        for client in client_list:
            client.send("Sync completed!".encode())

        print("All client objects created and forward method is called successfully.")

        for client in client_list:
            client.send("\n".encode())


if(__name__ == "__main__"):

    # connect_clients_process = Process(target= connect_clients)
    # connect_clients_process.start()

    connect_clients()