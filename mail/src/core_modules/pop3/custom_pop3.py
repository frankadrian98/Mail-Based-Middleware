import sys
import os
import threading
import socket

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from src.core_modules.exeptions.custom_exeptions import CustomConnectionError, UserDoesNotExists
from src.core_modules.databases.custom_database_handler import DatabaseHandler
from src.core_modules.smtp.custom_smtp import VALID_PORT_RANGE, is_valid_port, MAX_ALLOWED_CLIENT

POP3_COMMANDS = '''
    STAT – Count the number of emails.
    LIST – should list all the email for the user
    RETR – Retrieve email based on the serial number
    DELE – Should delete the email based on the serial number
    QUIT – Close the connection and terminate the program
'''

POP3_COMMANDS_LIST = ['STAT', 'LIST', 'RETR', 'DELE', 'QUIT']


class SimplePop3Server:
    def __init__(self,ip, port):
        self.host = ip
        self.port = port

    def __str__(self):
        return f'port: {self.port}'

    def __repr__(self):
        return f'SimplePop3Server Socket on port {self.port}'

    def connect(self):
        ''' This method creates a socket connection and binds to the port provided
            while instantiating object of SimplePop3Server class '''

        # logic for bind, gethostname, listen etc
        self.cur_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.host = socket.gethostname()
        # use localhost
        #self.host = ''
        try:
            self.cur_socket.bind((self.host, self.port))
            print(f'SimplePop3Server: Socket bound successfully on port {self.port} and ip {self.host if len(self.host) else "localhost"}')
        except socket.error as e:
            # raise CustomConnectionError (import form custom_errors) if error raised while connecting socket
            raise CustomConnectionError(e)

    def verify_loggedIn_user(self):
        '''
            This method verifies if the loggedIn user's data exists
            in the database (kind of authorization check)
        '''
        print(f'Verifying LoggedIn User Using POP3 Methods, Returning True without verifying')
        return True

    def operate_on_inbox(self):
        ''' Once the user is verified, this method is invoked. It provides
            client interface to check all mails in inbox, and delete them. '''

        print('Show user inbox and let operate for read/delete operation')

    def on_new_client(self, client_socket, client_address):
        '''
            On new connection from client, new thread is created and this method
            is invoked for the new client. This method handles client's queries
            about the inbox (reading/deleting mails)

            @param client_socket : Socket object used to send and recieve data
            @param client_address : address bound to socket on the other end of connection
        '''

        current_username = client_socket.recv(1024).decode('utf-8')
        print(f'SimplePop3Server: Recivied a connection from user {current_username} at {client_address}')
        try:
            current_user_data = DatabaseHandler().get_inbox_of(current_username)
        except UserDoesNotExists:
            current_user_data = dict()

        # While user doesn't types 'QUIT', keep taking request
        while True:
            user_response = client_socket.recv(1024).decode('utf-8')

            # on server side, print what user requested
            print(f'{current_username}\'s response: {user_response}')

            # if user requests something that is not in list of POP3_COMMANDS_LIST
            if user_response[:4] not in POP3_COMMANDS_LIST:
                client_socket.send(f'Command not identified. Please enter again.'.encode())
            elif user_response.startswith('STAT'):
                stat = str(len(current_user_data))
                client_socket.send(stat.encode())
            elif user_response.startswith('LIST'):
                mail_list = 'S.No.\t Sender\t\t DateTime\t\t Subject\n'
                for index, mail_ in enumerate(current_user_data):
                    mail_list += f'{index}\t {mail_["senders_email"]} {mail_["receiving_date_time"]} {mail_["subject"]} \n'
                client_socket.send(mail_list.encode())
            elif user_response.startswith('RETR'):
                try:
                    index = int(user_response.split()[-1])
                    mail_ = current_user_data[index]
                    mail_data = f' From: {mail_["senders_email"]}\n To: {current_username}@gmail.com\n Subject: {mail_["subject"]}\n DateTime: {mail_["receiving_date_time"]}\n Message: {mail_["message"]}\n'
                    client_socket.send(mail_data.encode())
                except Exception as e:
                    client_socket.send(f'Error {e} !'.encode())
            elif user_response.startswith('DEL'):       
                try:
                    index = int(user_response.strip().split()[-1])
                    # current_user_data.remove(index)
                    del current_user_data[index]
                    print(f'\tDeleting mail for {current_username} at index {index}')
                    DatabaseHandler().delete_mail(current_username, index)
                    client_socket.send(f'Deleted Successfully !'.encode())
                except Exception as e:
                    client_socket.send(f'Error {e} !'.encode())
            else:
                response = f'Thanks for connecting. Closing POP3 Server. Bye ^_^\n'
                client_socket.send(response.encode())
                client_socket.close()
                break            
        print(f'Client {current_username} disconnected.')

    def accept(self):
        ''' This method accepts connections from the clients and creates
         separate threads for each new client '''

        # logic for infinite loop reciving messages, handle keyboard error (user enters <C-D>, exit peacefully)
        self.cur_socket.listen(MAX_ALLOWED_CLIENT)

        print(f'SimplePop3Server: Waiting for connection on port {self.port} and ip {self.host if len(self.host) else "localhost"}')
        # Infinite loop to keep on listening for requests
        while True:
            try:
                client_socket, client_address = self.cur_socket.accept()
                threading._start_new_thread(self.on_new_client, (client_socket, client_address))
            except KeyboardInterrupt:
                print(f'\n\nKeyboard Interuption ! Closing server.\nThanks for connecting.')
                self.cur_socket.close()
                break
            except Exception as e:
                print(f'Some error occured. Closing Socket.')
                self.cur_socket.close()
                break