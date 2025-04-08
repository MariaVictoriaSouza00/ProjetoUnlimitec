from django.shortcuts import render, redirect
from .forms import CadastroEtapa1Form, CadastroEtapa2Form
from .models.usuario import Usuario
from .models import Cidade
from .models.endereco import Endereco
from django.http import JsonResponse




from django.shortcuts import render

from django.shortcuts import render, redirect

def login_usuario(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        if email.strip().lower() == 'maria-fallen@hotmail.com' and senha == 'senha123':
            return redirect('tela_index')  # redireciona para a tela do appPesquisa
        else:
            erro = 'E-mail ou senha incorretos.'
            return render(request, 'usuario/login.html', {'erro': erro})

    return render(request, 'usuario/login.html')


def cadastro_usuario(request):
    if request.method == 'POST':
        form = CadastroEtapa1Form(request.POST)
        if form.is_valid():
            # Pegando os dados do endereço
            logradouro = form.cleaned_data.pop('logradouro')
            cidade = form.cleaned_data.pop('cidade')

            # Criando o endereço
            endereco = Endereco.objects.create(logradouro=logradouro, cidade=cidade)

            # Criando o usuário
            usuario = form.save(commit=False)
            usuario.endereco = endereco
            usuario.set_password(form.cleaned_data['senha'])  # para salvar senha de forma segura
            usuario.save()

            return redirect('cadastro2')  # Vai para a próxima etapa
    else:
        form = CadastroEtapa1Form()
    return render(request, 'usuario/cadastro.html', {'form': form})


def cadastro_usuario_etapa2(request):
    if 'cadastro_etapa1' not in request.session:
        return redirect('cadastro_usuario')  # Volta se tentar acessar direto

    if request.method == 'POST':
        form = CadastroEtapa2Form(request.POST)
        if form.is_valid():
            # Cria usuário juntando dados da sessão e do formulário
            dados_etapa1 = request.session['cadastro_etapa1']
            usuario = Usuario(**dados_etapa1)
            usuario.set_password(dados_etapa1['senha'])
            
            # Adiciona campos da etapa 2
            for campo, valor in form.cleaned_data.items():
                setattr(usuario, campo, valor)

            usuario.save()
            request.session.pop('cadastro_etapa1', None)  # Limpa a sessão
            return redirect('login')  # Redireciona após cadastro
    else:
        form = CadastroEtapa2Form()

    return render(request, 'usuario/cadastro2.html', {'form': form})

    
def carregar_cidades(request):
    estado_id = request.GET.get('estado')
    cidades = Cidade.objects.filter(estado_id=estado_id).order_by('nome')
    cidades_json = [{'id': cidade.id, 'nome': cidade.nome} for cidade in cidades]
    return JsonResponse({'cidades': cidades_json})
