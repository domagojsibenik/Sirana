from django.contrib import admin
from .models import (
    NacinPlacanja,
    Sir,
    Narudzba,
    StavkaNarudzbe,
    Narucitelj,
    Zaposlenik,
    Dostavljac,
)


class StavkaNarudzbeInline(admin.TabularInline):
    model = StavkaNarudzbe
    extra = 1


@admin.register(Narudzba)
class NarudzbaAdmin(admin.ModelAdmin):
    list_display = ["id", "narucitelj", "status", "nacin_placanja", "vrKreiranja"]
    search_fields = ["narucitelj__naziv", "narucitelj__oib"]
    list_filter = ["status", "nacin_placanja"]
    inlines = [StavkaNarudzbeInline]


admin.site.register(NacinPlacanja)
admin.site.register(Sir)
admin.site.register(Narucitelj)
admin.site.register(Zaposlenik)
admin.site.register(Dostavljac)
