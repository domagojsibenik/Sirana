from django.contrib import admin
from .models import (
    NacinPlacanja,
    Sir,
    Narudzba,
    StavkaNarudzbe,
    Zaposlenik,
    Dostavljac
)


class StavkaNarudzbeInline(admin.TabularInline):
    model = StavkaNarudzbe
    extra = 1


@admin.register(Narudzba)
class NarudzbaAdmin(admin.ModelAdmin):
    list_display = ["id", "naziv_kupca", "status", "nacin_placanja", "vrKreiranja"]
    search_fields = ["id", "naziv_kupca"]
    list_filter = ["status", "nacin_placanja"]
    inlines = [StavkaNarudzbeInline]


admin.site.register(NacinPlacanja)
admin.site.register(Sir)
admin.site.register(Zaposlenik)
admin.site.register(Dostavljac)