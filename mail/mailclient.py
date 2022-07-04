import socket
import pickle
import argparse
import sys
from src.core_modules.smtp.custom_mail_template import Mail
from src.core_modules.databases.custom_database_handler import DatabaseHandler
from src.core_modules.exeptions.custom_exeptions import WrongEmailFormat, EmptySubject, UserDoesNotExists
from src.core_modules.clients.users import User

USER_OPTIONS = '''
    1.Manage Mail: Shows the stored mails of logged in user only
    2.Send Mail: Allows the user to send a mail
    3.Quit: Quits the program
'''


def authenticate_user():
    """Collects username and password

    Returns:
        User: an object of 'User' class 
    """
    username = input('Enter Name: ')
    password = input('Enter Password: ')
    user = User(username, password)

    while not user.is_authenticated:
        print('Wrong Credentials ! Try again.\n')
        username = input('Enter Name: ')
        password = input('Enter Password: ')
        user.update_credentials(username, password)

    return user


def interact_with_user(ip_list, smtp_port, pop_port):
    """Interacts with user providing them with various options to operate on
    their mail box.

    Args:
        ip (Int): Ip address for the connection
        port (Int): port number for the connection

    Raises:
        ValueError: If the user selects values different from given options
    """
    user = authenticate_user()

    while True:
        print(USER_OPTIONS)
        try:
            response = int(input('Your Choice: '))
            if response > 3 or response < 1:
                raise ValueError
            elif response == 1:
                user.operate_on_inbox(ip_list=ip_list, port=pop_port)
            elif response == 2:
                user.send_email(ip_list=ip_list, port=smtp_port)
            else:
                print(f'Process Terminating .....')
                sys.exit(0)
        except KeyboardInterrupt:
            print('Use Given Options To Exit !!')
        except ValueError:
            print('Enter valid values')
        except Exception as e:
            print(f'Error {e} occured')
            break


def Main():
    # For easy parsing of command line arguments
    parser = argparse.ArgumentParser(description='Command Line Argument Parser for client')

    #parser.add_argument('-ip', '--ip_address', type=str, help='IP Address to be connected to', required=True)
    parser.add_argument('-sp', '--smtp_port', type=int, help='Port of Smtp Server to be connected to', required=True)
    parser.add_argument('-pp', '--pop_port', type=int, help='Port of Pop Server to be connected to', required=True)


    # # Extract arguments passed from user, and verify the arguments are as expected
    args = parser.parse_args()

    with open('ip_addresses.txt') as ips:
        ip_adresses = ips.read().split('\n')
    smtp_port = args.smtp_port
    pop_port = args.pop_port

    interact_with_user(ip_adresses,smtp_port,pop_port)

if __name__ == '__main__':
    Main()
