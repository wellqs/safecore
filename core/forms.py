from django import forms
# --- ALTERAÇÃO 1: Adicionar 'ExposicaoRisco' ao import ---
from .models import Funcionario, AmbienteDeTrabalho, Cargo, ExposicaoRisco


class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        # Inclua todos os campos que você quer que apareçam no formulário de criação
        fields = [
            'nome_completo',
            'cpf',
            'empresa',
            'cargo',
            'data_admissao',
        ]
        # Opcional: Adicionar widgets para melhorar a aparência dos campos
        widgets = {
            'data_admissao': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'nome_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'empresa': forms.Select(attrs={'class': 'form-control'}),
            'cargo': forms.Select(attrs={'class': 'form-control'}),
        }


class AmbienteDeTrabalhoForm(forms.ModelForm):
    class Meta:
        model = AmbienteDeTrabalho
        fields = ['empresa', 'nome', 'descricao']
        widgets = {
            'empresa': forms.Select(attrs={'class': 'form-control'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class CargoForm(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = ['nome', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

# --- ALTERAÇÃO 2: Formulário para a Exposição de Risco (já estava presente, apenas validado) ---
class ExposicaoRiscoForm(forms.ModelForm):
    class Meta:
        model = ExposicaoRisco
        # Os campos 'cargo' e 'ambiente' serão preenchidos pela view, não pelo usuário
        fields = ['risco', 'intensidade', 'tecnica_utilizada']
        widgets = {
            'risco': forms.Select(attrs={'class': 'form-control'}),
            'intensidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 85 dB(A)'}),
            'tecnica_utilizada': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Dosimetria de ruído'}),
        }