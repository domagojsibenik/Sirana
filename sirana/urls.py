from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),

    path("nacini-placanja/", views.nacin_placanja_list, name="nacin_placanja_list"),
    path("nacini-placanja/dodaj/", views.nacin_placanja_create, name="nacin_placanja_create"),
    path("nacini-placanja/<int:pk>/uredi/", views.nacin_placanja_update, name="nacin_placanja_update"),
    path("nacini-placanja/<int:pk>/obrisi/", views.nacin_placanja_delete, name="nacin_placanja_delete"),

    path("sirevi/", views.sir_list, name="sir_list"),
    path("sirevi/dodaj/", views.sir_create, name="sir_create"),
    path("sirevi/<int:pk>/uredi/", views.sir_update, name="sir_update"),
    path("sirevi/<int:pk>/obrisi/", views.sir_delete, name="sir_delete"),

    path("narudzbe/", views.narudzba_list, name="narudzba_list"),
    path("narudzbe/dodaj/", views.narudzba_create, name="narudzba_create"),
    path("narudzbe/<int:pk>/", views.narudzba_detail, name="narudzba_detail"),
    path("narudzbe/<int:pk>/obrisi/", views.narudzba_delete, name="narudzba_delete"),

    path("narudzbe/<int:narudzba_id>/stavke/dodaj/", views.stavka_create, name="stavka_create"),
    path("stavke/<int:pk>/uredi/", views.stavka_update, name="stavka_update"),
    path("stavke/<int:pk>/obrisi/", views.stavka_delete, name="stavka_delete"),
]