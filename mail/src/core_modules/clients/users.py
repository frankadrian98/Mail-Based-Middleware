import os
import sys
import socket
import pickle
import time

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from src.core_modules.exeptions.custom_exeptions import CustomConnectionError, WrongEmailFormat, EmptySubject, UserDoesNotExists
from src.core_modules.databases.custom_database_handler import DatabaseHandler
from src.core_modules.smtp.custom_mail_template import Mail
from src.core_modules.pop3.custom_pop3 import POP3_COMMANDS


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.is_authenticated = DatabaseHandler().is_valid_user(username, password)

    def __str__(self):
        return f'user {self.username}'

    def __repr__(self):
        return self.__str__()

    def update_credentials(self, username, password):
        self.username = username
        self.password = password
        self.is_authenticated = DatabaseHandler().is_valid_user(username, password)

    def send_email(self, ip_list, port):
        """Create a connection with smtp server and take input, send
            import mail class]

        Args:
            ip (Int): ip address of the socket to which connection is to be 
                established for sending mail (smtp server)
            port (Int): port of the smtp server]
        """

        if not self.is_authenticated:
            print('Unauthenticated User. Cant send mail.')
            return None

        mail = Mail(self.username)
        # connect to smtp server (a socket in this case), and send mail object
        mail.take_email_input()
        for ip in ip_list:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect((ip, port))
            except Exception as e:
                print(f'Error while connecting to server at {ip}.')
                continue
            try:
                print(f'220 {ip if len(ip) else "127.0.0.1"}')
                print(f'C: HELO {ip if len(ip) else "127.0.0.1"}')
                print(f'S: 250 OK Hello {ip if len(ip) else "127.0.0.1"}')
                print(f'C: MAIL FROM: {mail.senders_email}')
                print(f'S: 250 {mail.senders_email}...Sender ok')
                print(f'C: RCPT TO: {mail.receivers_email}')
                print(f'S: 250 root...Recipient ok')
                print(f'C: {mail.message}')
                print(f'S: 250 OK Message accepted for delivery')
                print(f'C: QUIT')

                mail_as_string = pickle.dumps(mail)
                s.send(mail_as_string)
                print('Mail Sent Successfully.')
            except WrongEmailFormat:
                print('Please enter a valid email of the form : <username>@<domain name>')
            except EmptySubject:
                print('Subject Cant be empty !')
            except Exception as e:
                print(f'Error while sending mail: {e}')
            s.close()

    def operate_on_inbox(self, ip_list, port):
        """Provide various options to operate on one's inbox, like deleting,
            reading mails etc, connect to pop3 server and work

        Args:
            ip (Int): ip address of the socket to which connection is to be 
                established for sending mail (pop3 server)

            port (Int): port of the pop3 server
        """
        user_response = ''

        while not user_response.startswith('QUIT'):
            print(f'The available commands are: \n {POP3_COMMANDS}')
            user_response = input('Enter command: ')
            server_responses = []
            for ip in ip_list:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    s.connect((ip, port))
                    s.send(self.username.encode())
                    print(f'+OK POP3 Server ready at {ip}')
                    time.sleep(1)
                except UserDoesNotExists:
                    s.close()
                except Exception as e:
                    print(f'Error while connecting to server at {ip}.')
                    continue
                s.send(user_response.encode())
                server_response = s.recv(1024).decode('utf-8')
                #server_responses.append(server_response)
                print(server_response)
                # s.close()
                break
        print('goodbye.')
        
