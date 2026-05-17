from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Narudzba, NacinPlacanja, StatusNarudzbe, Narucitelj, Zaposlenik
from .services import NarudzbaService

class NarudzbaServiceTests(TestCase):

    def setUp(self):

        self.placanje_aktivno = NacinPlacanja.objects.create(
            naziv="Gotovina",
            aktivan=True
        )

        self.placanje_neaktivno = NacinPlacanja.objects.create(
            naziv="Virman",
            aktivan=False
        )

        self.narucitelj = Narucitelj.objects.create(
            naziv="Mamma Mia",
            oib="12345678901"
        )

        self.zaposlenik = Zaposlenik.objects.create(
            puno_ime="Ana Kundakčić"
        )
    
    def test_neaktivan_nacin_placanja_baca_gresku(self):
        """
        Baca grešku za korišten neaktivan način plaćanja
        """

        narudzba = Narudzba(
            narucitelj=self.narucitelj,
            zaposlenik=self.zaposlenik,
            nacin_placanja=self.placanje_neaktivno
        )

        with self.assertRaises(ValidationError):
            NarudzbaService.provjeri_aktivnost_placanja(narudzba)

    def test_aktivan_nacin_placanja_je_dozvoljen(self):
        """
        Ne baca grešku za korišten aktivan način plaćanja
        """

        narudzba = Narudzba(
            narucitelj=self.narucitelj,
            zaposlenik=self.zaposlenik,
            nacin_placanja=self.placanje_aktivno
        )

        try:
            NarudzbaService.provjeri_aktivnost_placanja(narudzba)

        except ValidationError:
            self.fail("Neočekivani ValidationError")

    def test_narudzba_u_obradi_se_ne_moze_uredivati(self):
        """
        Narudžba u obradi se ne smije moći uređivati
        """

        narudzba = Narudzba(
            narucitelj=self.narucitelj,
            zaposlenik=self.zaposlenik,
            nacin_placanja=self.placanje_aktivno,
            status=StatusNarudzbe.U_OBRADI
        )

        with self.assertRaises(ValidationError):

            NarudzbaService.provjeri_mogucnost_uredivanja(
                narudzba
            )

    def test_zaprimljena_narudzba_se_moze_uredivati(self):
        """
        Narudžba koja je ZAPRIMLJENA se može uređivati
        """

        narudzba = Narudzba(
            narucitelj=self.narucitelj,
            zaposlenik=self.zaposlenik,
            nacin_placanja=self.placanje_aktivno,
            status=StatusNarudzbe.ZAPRIMLJENA
        )

        try:
            NarudzbaService.provjeri_mogucnost_uredivanja(narudzba)

        except ValidationError:
            self.fail("Neočekivani ValidationError")