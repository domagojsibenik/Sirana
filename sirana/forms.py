from django import forms
from .models import NacinPlacanja, Sir, Narudzba, StavkaNarudzbe, Narucitelj
from django.forms import inlineformset_factory

class NaruciteljForm(forms.Form):
    naziv = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )

    adresa = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    telefon = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    oib = forms.CharField(
        max_length=11,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    def clean_oib(self):
        oib = self.cleaned_data.get("oib")

        if len(oib) != 11:
            raise forms.ValidationError("OIB mora imati točno 11 znamenki.")

        if not oib.isdigit():
            raise forms.ValidationError("OIB smije sadržavati samo znamenke.")

        return oib

class NacinPlacanjaForm(forms.ModelForm):
    class Meta:
        model = NacinPlacanja
        fields = ["naziv", "opis", "aktivan"]
        widgets = {
            "naziv": forms.TextInput(attrs={"class": "form-control"}),
            "opis": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "aktivan": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class SirForm(forms.ModelForm):
    class Meta:
        model = Sir
        fields = ["naziv", "cijena_po_kg", "kolicina_kg"]
        widgets = {
            "naziv": forms.TextInput(attrs={"class": "form-control"}),
            "cijena_po_kg": forms.NumberInput(attrs={"class": "form-control"}),
            "kolicina_kg": forms.NumberInput(attrs={"class": "form-control"}),
        }


class NarudzbaForm(forms.ModelForm):
    class Meta:
        model = Narudzba
        fields = [
            "nacin_placanja",
            "zaposlenik",
            "dostavljac",
            "napomena",
        ]
        widgets = {
            "nacin_placanja": forms.Select(attrs={"class": "form-select"}),
            "zaposlenik": forms.Select(attrs={"class": "form-select"}),
            "dostavljac": forms.Select(attrs={"class": "form-select"}),
            "napomena": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class StavkaNarudzbeForm(forms.ModelForm):
    class Meta:
        model = StavkaNarudzbe
        fields = ["sir", "kolicina_kg", "popust_postotak"]
        widgets = {
            "sir": forms.Select(attrs={"class": "form-select"}),
            "kolicina_kg": forms.NumberInput(attrs={"class": "form-control"}),
            "popust_postotak": forms.NumberInput(attrs={"class": "form-control"}),
        }


StavkaNarudzbeFormSet = inlineformset_factory(
    Narudzba,
    StavkaNarudzbe,
    form=StavkaNarudzbeForm,
    extra=3,
    can_delete=True
)
