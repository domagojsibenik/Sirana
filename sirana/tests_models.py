from decimal import Decimal

from django.test import TestCase
from .models import Narucitelj, Sir, StavkaNarudzbe, Narudzba, NacinPlacanja, Zaposlenik

class ModelTests(TestCase):
    def setUp(self):

        self.sir = Sir.objects.create(
            naziv="Bijeli",
            cijena_po_kg=Decimal("20"),
            kolicina_kg=Decimal("100")
        )

        self.placanje = NacinPlacanja.objects.create(
            naziv="Gotovina"
        )

        self.narucitelj = Narucitelj.objects.create(
            naziv="Mamma Mia",
            oib="12345678901"
        )

        self.zaposlenik = Zaposlenik.objects.create(
            puno_ime="Ivan Mažuranić"
        )

        self.narudzba = Narudzba.objects.create(
            narucitelj=self.narucitelj,
            zaposlenik=self.zaposlenik,
            nacin_placanja=self.placanje
        )

    def test_ukupno_bez_popusta(self):
        """
        Narudžba uspješno zbraja vrijednosti stavki
        """

        stavka = StavkaNarudzbe.objects.create(
            narudzba=self.narudzba,
            sir=self.sir,
            kolicina_kg=Decimal("2"),
            popust_postotak=Decimal("0")
        )

        stavka2 = StavkaNarudzbe.objects.create(
            narudzba=self.narudzba,
            sir=self.sir,
            kolicina_kg=Decimal("1"),
            popust_postotak=Decimal("0")
        )

        self.assertEqual(
            self.narudzba.ukupno(),
            Decimal("60")
        )

    def test_ukupno_s_popustom(self):
        """
        Narudžba uspješno stavlja popuste
        """

        stavka = StavkaNarudzbe.objects.create(
            narudzba=self.narudzba,
            sir=self.sir,
            kolicina_kg=Decimal("2"),
            popust_postotak=Decimal("10")
        )

        self.assertEqual(
            stavka.ukupno(),
            Decimal("36")
        )