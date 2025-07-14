from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PerfilUsuario, Psicologo

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, label="Nome")
    last_name = forms.CharField(max_length=30, required=True, label="Sobrenome")
    tipo = forms.ChoiceField(
        choices=PerfilUsuario.TIPO_CHOICES,
        widget=forms.RadioSelect,
        required=True,
        label="Tipo de usuário"
    )
    telefone = forms.CharField(max_length=15, required=False, label="Telefone")
    data_nascimento = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Data de nascimento"
    )
    
    # Campos específicos para psicólogos
    registro_crp = forms.CharField(
        max_length=20,
        required=False,
        label="Registro CRP",
        help_text="Obrigatório para psicólogos"
    )
    especialidades = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        label="Especialidades",
        help_text="Descreva suas áreas de especialização"
    )
    biografia = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False,
        label="Biografia profissional",
        help_text="Conte um pouco sobre sua experiência"
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adicionar classes CSS aos campos
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
        # Campos específicos para radio buttons
        self.fields['tipo'].widget.attrs['class'] = 'form-check-input'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email já está em uso.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        registro_crp = cleaned_data.get('registro_crp')
        
        # Validar campos obrigatórios para psicólogos
        if tipo == 'psicologo' and not registro_crp:
            raise forms.ValidationError("Registro CRP é obrigatório para psicólogos.")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            
            # Atualizar perfil do usuário
            perfil = user.perfil
            perfil.tipo = self.cleaned_data['tipo']
            perfil.telefone = self.cleaned_data.get('telefone', '')
            perfil.data_nascimento = self.cleaned_data.get('data_nascimento')
            perfil.save()
            
            # Criar dados específicos para psicólogos
            if self.cleaned_data['tipo'] == 'psicologo':
                Psicologo.objects.create(
                    user=user,
                    nome=f"{user.first_name} {user.last_name}",
                    email=user.email,
                    registro_crp=self.cleaned_data['registro_crp'],
                    especialidades=self.cleaned_data.get('especialidades', ''),
                    biografia=self.cleaned_data.get('biografia', '')
                )
        
        return user

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome de usuário'
        }),
        label="Nome de usuário"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Senha'
        }),
        label="Senha"
    )

