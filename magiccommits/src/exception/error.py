class KnownError(Exception):
    pass

class NetworkError(Exception):
    def __init__(self, error_dict):
        self.error = error_dict

class UnKnownError(Exception):

    def __init__(self,message):
        self.message = message

def error(message: str):
    raise KnownError(message)