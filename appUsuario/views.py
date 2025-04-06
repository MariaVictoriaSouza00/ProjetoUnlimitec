from django.shortcuts import render, redirect
from django import forms
from .models.usuario import Usuario  # ou from .models import Usuario, dependendo da estrutura
from django.contrib.auth import authenticate, login

class UsuarioForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput())  # deixa a senha oculta

    class Meta:
        model = Usuario
        fields = [
            'nome', 'email', 'senha', 'celular',
            'grau_escolaridade', 'instituicao_ensino',
            'area_interesse', 'profissao', 'endereco'
        ]

def cadastro_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.set_password(form.cleaned_data['senha'])
            usuario.save()
            return redirect('login')  # ou qualquer outra página
    else:
        form = UsuarioForm()

    return render(request, 'usuario/cadastro.html', {'form': form})



class LoginForm(forms.Form):
    email = forms.EmailField(label="E-mail")
    senha = forms.CharField(widget=forms.PasswordInput(), label="Senha")

def login_usuario(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            senha = form.cleaned_data['senha']

            try:
                usuario = Usuario.objects.get(email=email)
                if usuario.check_password(senha):  # ← verifica a senha usando método do Django
                    # Aqui você pode usar login(request, usuario) se for um User válido
                    return redirect('pagina_principal')  # ou outra página
                else:
                    form.add_error(None, 'Senha incorreta.')
            except Usuario.DoesNotExist:
                form.add_error(None, 'Usuário não encontrado.')
    else:
        form = LoginForm()
    
    return render(request, 'usuario/login.html', {'form': form})