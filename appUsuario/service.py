from appUsuario.models import Usuario, Endereco, Cidade, UF, Escolaridade
from django.core.exceptions import ValidationError

def criar_usuario(nome, email, data_nascimento, endereco_id, escolaridade_id, senha):
    """Cria um novo usuário com as regras de negócio"""
    
    if Usuario.objects.filter(email=email).exists():
        raise ValidationError("Já existe um usuário com este e-mail.")

    endereco = Endereco.objects.filter(id=endereco_id).first()
    escolaridade = Escolaridade.objects.filter(id=escolaridade_id).first()
    
    if not endereco:
        raise ValidationError("Endereço inválido.")
    if not escolaridade:
        raise ValidationError("Escolaridade inválida.")

    usuario = Usuario.objects.create_user(
        nome=nome,
        email=email,
        username=email,  # Usa o email como username
        data_nascimento=data_nascimento,
        endereco=endereco,
        escolaridade=escolaridade,
        password=senha  # Senha precisa ser tratada com hash (Django já faz isso)
    )
    return usuario
