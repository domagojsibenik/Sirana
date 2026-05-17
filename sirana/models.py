from django.db import models
from decimal import Decimal


class NacinPlacanja(models.Model):
    naziv = models.CharField(max_length=100)
    opis = models.TextField(blank=True)
    aktivan = models.BooleanField(default=True)

    def __str__(self):
        return self.naziv

class Narucitelj(models.Model):
    naziv = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    adresa = models.CharField(max_length=200, blank=True)
    telefon = models.CharField(max_length=30, blank=True)
    oib = models.CharField(max_length=11, unique=True)

    def __str__(self):
        return self.naziv
    
class Sir(models.Model):
    naziv = models.CharField(max_length=100)
    cijena_po_kg = models.DecimalField(max_digits=10, decimal_places=2)
    kolicina_kg = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    zaProdaju = models.BooleanField(default=True)

    def __str__(self):
        return self.naziv

class Zaposlenik(models.Model):
    puno_ime = models.CharField(max_length=100)
    datumZaposlenja = models.DateTimeField(auto_now_add=True)
    statusRada = models.CharField(max_length=100)

    def __str__(self):
        return self.puno_ime

class Dostavljac(models.Model):
    naziv = models.CharField(max_length=100)
    opis = models.TextField(blank=True)

    def __str__(self):
        return self.naziv

class StatusNarudzbe(models.TextChoices):
    ZAPRIMLJENA = "zaprimljena", "Zaprimljena"
    U_OBRADI = "u_obradi", "U obradi"
    ISPORUCENA = "isporucena", "Isporučena"
    OTKAZANA = "otkazana", "Otkazana"


class Narudzba(models.Model):
    vrKreiranja = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=StatusNarudzbe.choices,default=StatusNarudzbe.ZAPRIMLJENA)
    napomena = models.TextField(blank=True)

    
    narucitelj = models.ForeignKey(Narucitelj, on_delete=models.PROTECT)
    

    nacin_placanja = models.ForeignKey(NacinPlacanja, on_delete=models.PROTECT)

    zaposlenik = models.ForeignKey(
        Zaposlenik,
        related_name="narudzbe",
        on_delete=models.PROTECT
    )
    
    dostavljac = models.ForeignKey(Dostavljac, on_delete=models.PROTECT)
    

    def ukupno(self):
        return sum(stavka.ukupno() for stavka in self.stavke.all())



class StavkaNarudzbe(models.Model):
    narudzba = models.ForeignKey(
        Narudzba,
        related_name="stavke",
        on_delete=models.CASCADE
    )

    sir = models.ForeignKey(Sir, on_delete=models.PROTECT)
    kolicina_kg = models.DecimalField(max_digits=10, decimal_places=2)
    cijena_po_kg = models.DecimalField(max_digits=10, decimal_places=2)
    popust_postotak = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def ukupno(self):
        osnovica = self.kolicina_kg * self.sir.kolicina_kg * self.sir.cijena_po_kg
        popust = osnovica * self.popust_postotak / Decimal("100")
        return osnovica - popust

    def __str__(self):
        return f"{self.sir.naziv} - {self.kolicina_kg} kg"
    



