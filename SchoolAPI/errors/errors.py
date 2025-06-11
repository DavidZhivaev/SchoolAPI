class TokenError(Exception):
    def __init__(self, message=None):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"Token {self.message} is broken, change it!" if self.message else "Token is broken, change it!"
    
class DnevnikError(Exception):
    def __init__(self, message: str=None):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"Dnevnik error!\n{self.message}!" if self.message else "Dnevnik error!"
    
class LibError(Exception):
    def __init__(self, message: str=None):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"Library error!\n{self.message}!" if self.message else "Library error!"