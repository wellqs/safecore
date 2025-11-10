from django import forms
from django.forms import inlineformset_factory
from .models import Relatorio, RelatorioAtividade


class RelatorioForm(forms.ModelForm):
    class Meta:
        model = Relatorio
        fields = ["titulo", "data", "observacao"]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "data": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "observacao": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }


RelatorioAtividadeFormSet = inlineformset_factory(
    Relatorio,
    RelatorioAtividade,
    fields=("contador",),
    extra=0,
    can_delete=False,
    widgets={
        "contador": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
    },
)

