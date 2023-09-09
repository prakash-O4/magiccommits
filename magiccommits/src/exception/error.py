class KnownError(Exception):
    pass

def error(message: str):
    raise KnownError(message)