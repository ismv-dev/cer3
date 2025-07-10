from django import forms
from .models import Taller
from api.feriado import dataFeriado
from datetime import date
from django.core.exceptions import ValidationError

class TallerAdminForm(forms.ModelForm):
    class Meta:
        model = Taller
        fields = '__all__'
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'min': date.today().strftime('%Y-%m-%d'), 'class': 'form-control'}),
            'duracion_horas': forms.NumberInput(attrs={'min': 0, 'step': 'any', 'class': 'form-control'}),
        }

    def clean(self):
        data = super().clean()
        try:
            data = dataFeriado(data)
        except Exception as e:
            raise ValidationError(f"Error en validación de fecha: {str(e)}")
        return data

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu usuario',
            'autocomplete': 'username',
        })
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'id': 'password',
            'class': 'form-control',
            'placeholder': 'Ingresa tu contraseña',
            'autocomplete': 'current-password',
        })
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError("El nombre de usuario es obligatorio.")
        # Sanitize username input
        username = username.strip()
        if len(username) < 3:
            raise forms.ValidationError("El nombre de usuario debe tener al menos 3 caracteres.")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError("La contraseña es obligatoria.")
        if len(password) < 8:
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        return password

class TallerForm(forms.ModelForm):
    class Meta:
        model = Taller
        fields = '__all__'
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'min': date.today().strftime('%Y-%m-%d'), 'class': 'form-control'}),
            'duracion_horas': forms.NumberInput(attrs={'min': 0, 'step': 'any', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        if self.request and not self.request.user.is_staff:
            for campo in ['estado', 'observacion']:
                if campo in self.fields:
                    self.fields[campo].disabled = True

    def clean(self):
        cleaned_data = super().clean()
        try:
            cleaned_data = dataFeriado(cleaned_data)
        except Exception as e:
            raise ValidationError(f"Error en validación de fecha: {str(e)}")
        return cleaned_data

    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo')
        if titulo:
            titulo = titulo.strip()
            if len(titulo) < 5:
                raise forms.ValidationError("El título debe tener al menos 5 caracteres.")
        return titulo

    def clean_duracion_horas(self):
        duracion = self.cleaned_data.get('duracion_horas')
        if duracion is not None and duracion <= 0:
            raise forms.ValidationError("La duración debe ser mayor a 0 horas.")
        if duracion is not None and duracion > 24:
            raise forms.ValidationError("La duración no puede exceder 24 horas.")
        return duracion