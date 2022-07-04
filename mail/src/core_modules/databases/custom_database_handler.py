import pickle
import json
import os
import sys
from datetime import datetime

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from src.core_modules.exeptions.custom_exeptions import UserDoesNotExists

DATABASE_FORMAT = '''
    {
        "Credentials":{
            "name":"password"
        },
        "Mails":{
            "name":[
                {
                    "senders_email":"sender@gmail.com",
                    "receiving_date_time":"12/02/2022,02:23",
                    "subject":"trial mail",
                    "message":"this is a trial mail"
                }
            ]
        }
    }
'''

# update this path using os modules
current_dir = os.path.dirname(os.path.realpath(__file__))
DATABASE_PATH = os.path.join(current_dir, 'database.json')


class DatabaseHandler:
    ''' This class provides methods to query/update/delete data from database.json (used as database here) '''

    database = '_'

    def __init__(self):
        self.load_data()

    @classmethod
    def load_data(cls):
        # load json data form database for easy modification
        with open(DATABASE_PATH) as f:
            cls.database = json.load(f)

    def __str__(self):
        return 'DatabaseHandler Object'

    def __repr__(self):
        return self.__str__()

    @classmethod
    def is_valid_user(cls, username, password):
        """ checks if given credentials are valid.

        Args:
            username (str): Username
            password (str): Password

        Returns:
            [Bool]: If user is valid
        """
        cls.load_data()
        if username not in cls.database['Credentials']:
            return False
        elif cls.database['Credentials'][username] != password:
            return False
        return True

    @staticmethod
    def verify_or_create(receivers_email):
        ''' check if workspace for user whose email address is provided exists
         if it doesn't exists, create one such '''

        print(f'Verifying existence of email {receivers_email}')

    @classmethod
    def save_mail(cls, mail):
        ''' Recieves a Mail object sterlised by pickle, and saves it at 
        corresponding place '''

        # check for format and dump it to json file
        mail = pickle.loads(mail)
        print(f'\nRecieved mail: \n From: {mail.username}\n To: {mail.receivers_email}\n About: {mail.subject}\n Details: {mail.message}\n')

        DatabaseHandler.verify_or_create(mail.receivers_email)

        # Now as workspace presence is confirmed, dump the email data to the database
        
        if mail.username not in cls.database['Mails'].keys() and mail.username not in cls.database['Credentials'].keys():
            cls.database['Mails'][mail.username] = list()
            

        mail_as_dict = dict()
        mail_as_dict['senders_email'] = mail.senders_email
        mail_as_dict['receiving_date_time'] = f'{datetime.now().replace(microsecond=0)}' 
        mail_as_dict['subject'] = mail.subject
        mail_as_dict['message'] = mail.message

        cls.database['Mails'][mail.username].append(mail_as_dict)
        print(f'Saving the mail.')

        with open(DATABASE_PATH, 'w') as f:
            json.dump(cls.database, f, indent=4)
        print(f'Mail Successfully Saved.\n')
        cls.dump_all()

    @classmethod
    def get_inbox_of(cls, username):
        ''' returns list of all mails of the user provided as argument '''

        cls.load_data()
        if username not in cls.database['Mails']:
            raise UserDoesNotExists('Given User Does Not Exists')
        return cls.database['Mails'][username]

    @classmethod
    def delete_mail(cls, username, mail_index):
        cls.load_data()
        try:
            del cls.database['Mails'][username][mail_index]
        except ValueError:
            print('The mail does not seem to be existing')

        # update the actual database i.e. database.json
        with open(DATABASE_PATH, 'w') as f:
            json.dump(cls.database, f, indent=4)
        print(f'\tMail for user {username} at index {mail_index} deleted Successfully.')
        cls.dump_all()

    @classmethod
    def dump_all(cls):
        ''' Dumps the data (after transaction from user) to the respective 
        text file '''

        mails = cls.database['Mails']
        for user in mails:
            try:
                if not os.path.isdir(f'{current_dir}/users/{user}/'):
                    os.mkdir(f'{current_dir}/users/{user}/')
                with open(f'{current_dir}/users/{user}/Inbox.txt', 'w') as f:
                    for user_mail in mails[user]:
                        f.write(f'To: {user}@gmail.com\n')
                        for key, val in user_mail.items():
                            f.write(str(key) + ': ' + str(val) + '\n')
                        f.write('.\n')
            except Exception as e:
                print(f' exception {e}')
