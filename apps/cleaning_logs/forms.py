"""
Forms for cleaning log registration
"""
from django import forms
from .models import CleaningLog


class PublicCleaningLogForm(forms.ModelForm):
    """
    Simplified form for public cleaning log registration via QR code
    No authentication required - equipment identified by token
    """

    class Meta:
        model = CleaningLog
        fields = ['photo', 'notes']
        widgets = {
            'photo': forms.FileInput(attrs={
                'accept': 'image/*',
                'capture': 'environment',  # Open camera on mobile
                'class': 'hidden',
                'id': 'photo-input',
                'x-ref': 'photoInput',
            }),
            'notes': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Adicione observações sobre a limpeza (opcional)',
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'maxlength': 500,
            }),
        }
        labels = {
            'photo': 'Foto Comprobatória',
            'notes': 'Observações',
        }
        help_texts = {
            'photo': 'Tire uma foto do equipamento após a limpeza',
            'notes': 'Adicione detalhes relevantes sobre a limpeza realizada',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Photo is required for public registration
        self.fields['photo'].required = True
        self.fields['notes'].required = False

    def clean_photo(self):
        """Validate photo upload"""
        photo = self.cleaned_data.get('photo')

        if not photo:
            raise forms.ValidationError('A foto é obrigatória para comprovar a limpeza.')

        # Validate file size (max 10MB)
        if photo.size > 10 * 1024 * 1024:
            raise forms.ValidationError('A foto não pode ter mais de 10MB.')

        # Validate file type
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
        if photo.content_type not in allowed_types:
            raise forms.ValidationError('Formato de imagem inválido. Use JPEG, PNG ou WebP.')

        return photo

    def clean_notes(self):
        """Clean and validate notes"""
        notes = self.cleaned_data.get('notes', '').strip()

        # Remove excessive whitespace
        notes = ' '.join(notes.split())

        return notes
