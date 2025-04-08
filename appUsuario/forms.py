from django import forms
from .models.usuario import Usuario
from .models.cidade import Cidade
from .models.endereco import Endereco
from .models.estado import Estado

class CadastroEtapa1Form(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput(), label="Senha")
    
    estado = forms.ModelChoiceField(
        queryset=Estado.objects.all(),
        required=False,
        empty_label="SELECIONE"
    )
    cidade = forms.ModelChoiceField(
        queryset=Cidade.objects.none(),
        required=False,
        empty_label="SELECIONE"
    )
    logradouro = forms.CharField(max_length=255, label="Logradouro")

    class Meta:
        model = Usuario
        fields = ['nome', 'email', 'senha', 'celular']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['estado'].queryset = Estado.objects.all()
        self.fields['cidade'].queryset = Cidade.objects.none()

        if 'estado' in self.data:
            try:
                estado_id = int(self.data.get('estado'))
                self.fields['cidade'].queryset = Cidade.objects.filter(estado_id=estado_id).order_by('nome')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.endereco:
            self.fields['cidade'].queryset = self.instance.endereco.cidade.estado.cidade_set.order_by('nome')

# Etapa 2: Dados educacionais/profissionais
class CadastroEtapa2Form(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'grau_escolaridade',
            'instituicao_ensino',
            'area_interesse',
            'profissao'
        ]
