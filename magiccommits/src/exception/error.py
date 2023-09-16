class KnownError(Exception):
    pass

class NetworkError(Exception):
    pass

def error(message: str):
    raise KnownError(message)