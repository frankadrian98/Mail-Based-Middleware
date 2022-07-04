import os
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from src.core_modules.exeptions.custom_exeptions import MailInputUnsuccessful, WrongEmailFormat, EmptySubject

class Mail:
    def __init__(self, username):
        self.username = username

    def __str__(self):
        return self.username
    
    def __repr__(self):
        return f'Mail by {self.username}'

    def is_valid_email_address(self, given_email):
        '''
            Checks if given email address is valid
        '''
        if not '@' in given_email:
            return False
        elif given_email.startswith('@') or given_email.endswith('@'):
            return False
        return True

    def update_username(self, senders_email):
        self.username = senders_email.split('@')[0]

    def take_email_input(self):
        '''
            Accepts input mail from user, and verifies the format of mail
            raises MailInputUnsuccessful error upon keyboard inturuption without
            completing input for current mail

            Input for subject terminates when a '.\n' is recieved
        '''
        self.senders_email = input('From: ')
        self.receivers_email = input('To: ')

        self.subject = input('Subject: ')
        self.message, message_block = '', ''
        print('Message: ', end='')
        while message_block != '.':
            self.message += message_block
            message_block = input()

        if not self.is_valid_email_address(self.receivers_email) or not self.is_valid_email_address(self.senders_email):
            raise WrongEmailFormat('Wrong Email Format')
        elif len(self.subject.strip()) == 0:
            raise EmptySubject('Subject is empty')

        self.update_username(self.receivers_email.split('@')[0])