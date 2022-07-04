import sys
import os
import threading
import socket
import pickle

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from src.core_modules.exeptions.custom_exeptions import CustomConnectionError
from src.core_modules.databases.custom_database_handler import DatabaseHandler


# range of valid port range that can be used for socket connection
VALID_PORT_RANGE = [1024, 65535]

MAX_ALLOWED_CLIENT = 5


def is_valid_port(port):
    """
        Function to check if given port is allowed for socket to be connected

        @param port : int denoting the port to be connected
        return : boolean denoting if passed port number is valid
    """

    start, end = VALID_PORT_RANGE
    # check if port is an int
    try:
        port = int(port)
    except ValueError:
        return False
    except Exception as e:
        print(f"Exeption caught while checking validity of port {e}")
        return False

    # check if port is in valid range
    if port >= start and port <= end:
        return True
    return False


class SimpleMailServer:
    def __init__(self, ip,port):
        self.host = ip
        self.port = port

    def __str__(self):
        return f"port: {self.port}"

    def __repr__(self):
        return f"SimpleMailServer Socket on port {self.port}"

    def connect(self):
        """
            This method creates a socket connection and binds to the port provided
            while instantiating object of SimpleMailServer class
        """
        # logic for bind, gethostname, listen etc
        self.cur_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # leave blank for localhost
        # self.host = ""
        try:
            self.cur_socket.bind((self.host, self.port))
            print(f'SimpleMailServer: Socket bound successfully on port {self.port} and ip {self.host if len(self.host) else "localhost"}')
        except socket.error as e:
            raise CustomConnectionError(e)

    def on_new_client(self, client_socket, client_address):
        """
            On new connection from client, new thread is created and this method
            is invoked for the new client. This method accepts data from the client
            and sends it to DatabaseHandler to update inbox of the person, to whom
            the mail is sent

            @param client_socket : Socket object used to send and recieve data
            @param client_address : address bound to socket on the other end of connection
        """

        print(f"SimpleMailServer: Recivied a connection from {client_address}")
        mail = client_socket.recv(1024)
        cur_mail = pickle.loads(mail)

        print(f'C: HELO {self.host if len(self.host) else "127.0.0.1"}')
        print(f'S: 250 OK Hello {self.host if len(self.host) else "127.0.0.1"}')
        print(f"C: MAIL FROM: {cur_mail.senders_email}")
        print(f"S: 250 {cur_mail.senders_email}...Sender ok")
        print(f"C: RCPT TO: {cur_mail.receivers_email}")
        print(f"S: 250 root...Recipient ok")
        print(f"C: {cur_mail.message}")
        print(f"S: 250 OK Message accepted for delivery")
        print(f"C: QUIT")

        # check for error if no such user exists
        DatabaseHandler().save_mail(mail)
        client_socket.close()

    def accept(self):
        """ This method accepts connections from the clients and creates
         separate threads for each new client """

        self.cur_socket.listen(MAX_ALLOWED_CLIENT)

        print(f"SimpleMailServer: Waiting for connection on port {self.port}")
        # logic for infinite loop reciving messages, handle keyboard error (user enters <C-D>, exit peacefully)
        while True:
            try:
                client_socket, client_address = self.cur_socket.accept()
                threading._start_new_thread(self.on_new_client, (client_socket, client_address))
            except KeyboardInterrupt:
                print(f"\n\nKeyboard Interuption ! Closing server.\nThanks for connecting.")
                self.cur_socket.close()
                break
            except Exception as e:
                print(f"Some error occured. Closing Socket.")
                self.cur_socket.close()
                break
