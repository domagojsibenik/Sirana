from django.db import models
from decimal import Decimal


class NacinPlacanja(models.Model):
    naziv = models.CharField(max_length=100)
    opis = models.TextField(blank=True)
    aktivan = models.BooleanField(default=True)

    def __str__(self):
        return self.naziv


class Sir(models.Model):
    naziv = models.CharField(max_length=100)
    cijena_po_kg = models.DecimalField(max_digits=10, decimal_places=2)
    kolicina_kg = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.naziv


class StatusNarudzbe(models.TextChoices):
    ZAPRIMLJENA = "zaprimljena", "Zaprimljena"
    U_OBRADI = "u_obradi", "U obradi"
    ISPORUCENA = "isporucena", "Isporučena"
    OTKAZANA = "otkazana", "Otkazana"


class Narudzba(models.Model):
    naziv_kupca = models.CharField(max_length=100)
    email_kupca = models.EmailField(blank=True)
    adresa_kupca = models.CharField(max_length=200, blank=True)
    telefon_kupca = models.CharField(max_length=30, blank=True)
    oib_kupca = models.CharField(max_length=11, blank=True)

    status = models.CharField(
        max_length=20,
        choices=StatusNarudzbe.choices,
        default=StatusNarudzbe.ZAPRIMLJENA
    )

    nacin_placanja = models.ForeignKey(
        NacinPlacanja,
        on_delete=models.PROTECT
    )

    datum = models.DateTimeField(auto_now_add=True)
    napomena = models.TextField(blank=True)

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