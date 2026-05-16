from django.core.exceptions import ValidationError

from .models import StatusNarudzbe


class NarudzbaService:
    @staticmethod
    def provjeri_aktivnost_placanja(narudzba):
        if narudzba.nacin_placanja and not narudzba.nacin_placanja.aktivan:
            raise ValidationError(
                "Nije moguće kreirati narudžbu s neaktivnim načinom plaćanja."
            )

    @staticmethod
    def provjeri_mogucnost_uredivanja(narudzba):
        if narudzba.status == StatusNarudzbe.U_OBRADI:
            raise ValidationError(
                "Narudžba u procesu proizvodnje više se ne može uređivati."
            )