class ValidationError(Exception):
    def __init__(self, message: str, errors: list = None): super().__init__(message); self.errors = errors or []
class SecurityError(Exception): pass