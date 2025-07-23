from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom JWT Authentication class if you need to add extra behavior.
    For now, it just uses the standard JWTAuthentication.
    """
    pass
