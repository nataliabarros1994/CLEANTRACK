"""
Custom authentication backend for email-based login
"""
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailBackend(ModelBackend):
    """
    Backend de autenticação customizado que permite login por email.
    Também mantém compatibilidade com login por username.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Autentica usando email ou username.
        O parâmetro 'username' pode conter email ou username real.
        """
        if username is None or password is None:
            return None

        try:
            # Tentar primeiro por email
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            # Se não encontrar por email, tentar por username
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # Run the default password hasher once to reduce the timing
                # difference between an existing and a nonexistent user
                User().set_password(password)
                return None

        # Verificar se a senha está correta e se o usuário pode autenticar
        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None

    def get_user(self, user_id):
        """Obtém usuário por ID"""
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
