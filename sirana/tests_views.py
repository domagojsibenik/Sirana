from django.test import TestCase
from django.urls import reverse

from .models import NacinPlacanja, Narudzba, Zaposlenik

class ViewTests(TestCase):
    def setUp(self):

        self.placanje = NacinPlacanja.objects.create(
            naziv="Gotovina",
            aktivan=True
        )

        self.zaposlenik = Zaposlenik.objects.create(
            puno_ime="Dmitar Zvonimir"
        )

    def test_create_narudzba(self):
        """
        Moguće stvoriti narudžbu pomoću POST naredbe
        """

        response = self.client.post(
            reverse("narudzba_create"),
            {
                "naziv": "Restoran Mamma Mia",
                "email": "RestoranMammaMia@yahoo.com",
                "adresa": "Ferovac 3",
                "telefon": "099 123 4567",
                "oib": "12345678901",

                "nacin_placanja": self.placanje.id,
                "zaposlenik": self.zaposlenik.id,
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Narudzba.objects.count(), 1)
        
    def test_create_page_loads(self):
        """
        Stranica za ucitavanje narudzbe radi.
        """

        response = self.client.get(
            reverse("narudzba_create")
        )

        self.assertEqual(response.status_code, 200)
