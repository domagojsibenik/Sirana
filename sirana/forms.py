from django import forms
from .models import NacinPlacanja, Sir, Narudzba, StavkaNarudzbe
from django.forms import inlineformset_factory


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
            "naziv_kupca",
            "email_kupca",
            "adresa_kupca",
            "telefon_kupca",
            "oib_kupca",
            "nacin_placanja",
            "napomena",
        ]
        widgets = {
            "naziv_kupca": forms.TextInput(attrs={"class": "form-control"}),
            "email_kupca": forms.EmailInput(attrs={"class": "form-control"}),
            "adresa_kupca": forms.TextInput(attrs={"class": "form-control"}),
            "telefon_kupca": forms.TextInput(attrs={"class": "form-control"}),
            "oib_kupca": forms.TextInput(attrs={"class": "form-control"}),
            "nacin_placanja": forms.Select(attrs={"class": "form-select"}),
            "napomena": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class StavkaNarudzbeForm(forms.ModelForm):
    class Meta:
        model = StavkaNarudzbe
        fields = ["sir", "kolicina_kg", "cijena_po_kg", "popust_postotak"]
        widgets = {
            "sir": forms.Select(attrs={"class": "form-select"}),
            "kolicina_kg": forms.NumberInput(attrs={"class": "form-control"}),
            "cijena_po_kg": forms.NumberInput(attrs={"class": "form-control"}),
            "popust_postotak": forms.NumberInput(attrs={"class": "form-control"}),
        }


StavkaNarudzbeFormSet = inlineformset_factory(
    Narudzba,
    StavkaNarudzbe,
    form=StavkaNarudzbeForm,
    extra=3,
    can_delete=True
)
