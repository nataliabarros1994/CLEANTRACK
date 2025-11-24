from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    """
    Formulário de criação de usuário customizado para usar email como identificador.
    """
    email = forms.EmailField(
        required=True,
        help_text='Required. Enter a valid email address.'
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'username')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Tornar username opcional (será gerado automaticamente se vazio)
        self.fields['username'].required = False
        self.fields['username'].help_text = 'Optional. Will be auto-generated from email if left blank.'

    def clean_username(self):
        """Auto-gerar username a partir do email se não fornecido"""
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if not username and email:
            # Gerar username a partir do email
            username = email.split('@')[0]
            # Garantir que seja único
            base_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1

        return username


class CustomUserChangeForm(UserChangeForm):
    """
    Formulário de edição de usuário customizado para usar email como identificador.
    """

    class Meta:
        model = User
        fields = '__all__'
