from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    
    email = forms.EmailField(required=True, label="Correo electrónico")  # Campo de correo electrónico
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agrega clases CSS o atributos personalizados a los campos del formulario
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'custom-input',
                'placeholder': self.fields[field_name].label
            })
        
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')  # Incluye el campo de correo
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']  # Guarda el correo en el modelo
        if commit:
            user.save()
        return user