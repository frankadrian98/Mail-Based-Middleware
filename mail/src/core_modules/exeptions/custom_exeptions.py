# Module for different custom classes, as different errors need to be handled differently

class CustomConnectionError(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg


class MailInputUnsuccessful(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class WrongEmailFormat(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class EmptySubject(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class UserDoesNotExists(Exception):
    def __init__(self, msg):
        super().__init__(msg)
