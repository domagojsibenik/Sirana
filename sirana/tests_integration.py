from django.test import TestCase
from django.urls import reverse
from .models import Sir, NacinPlacanja, Narudzba, StavkaNarudzbe, Zaposlenik

class IntegrationTests(TestCase):
    def test_full_order_creation(self):
        """
        Ispituje potpuno stvaranje narudžbe
        """

        placanje = NacinPlacanja.objects.create(
            naziv="Kartica",
            aktivan=True
        )

        zaposlenik = Zaposlenik.objects.create(
            puno_ime="Ivan Mažuranić"
        )

        sir = Sir.objects.create(
            naziv="Bijeli",
            cijena_po_kg=10,
            kolicina_kg=50
        )

        response = self.client.post(
            reverse("narudzba_create"),
            {
                "naziv": "Restoran Mamma Mia",
                "email": "RMM@gmail.com",
                "adresa": "Ferovac 3",
                "telefon": "123456",
                "oib": "12345678901",

                "nacin_placanja": placanje.id,
                "zaposlenik": zaposlenik.id,

                "sir_id[]": [sir.id],
                "kolicina_kg[]": ["4"],
                "popust_postotak[]": ["0"],
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Narudzba.objects.count(), 1)
        self.assertEqual(StavkaNarudzbe.objects.count(), 1)

        moja_narudzba = Narudzba.objects.first()

        self.assertEqual(moja_narudzba.ukupno(), 40)