from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from decimal import Decimal
from .models import NacinPlacanja, Sir, Narudzba, StavkaNarudzbe
from .forms import (
    NacinPlacanjaForm,
    SirForm,
    NarudzbaForm,
    StavkaNarudzbeForm,
    StavkaNarudzbeFormSet,
)
from django.core.exceptions import ValidationError
from .services import NarudzbaService

def home(request):
    return render(request, "sirana/home.html")



def nacin_placanja_list(request):
    search = request.GET.get("search", "")

    nacini = NacinPlacanja.objects.all()

    if search:
        nacini = nacini.filter(naziv__icontains=search)

    return render(request, "sirana/nacin_placanja_list.html", {
        "nacini": nacini,
        "search": search,
    })


def nacin_placanja_create(request):
    if request.method == "POST":
        form = NacinPlacanjaForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Način plaćanja je dodan.")
            return redirect("nacin_placanja_list")
    else:
        form = NacinPlacanjaForm()

    return render(request, "sirana/form.html", {
        "form": form,
        "title": "Dodaj način plaćanja",
    })


def nacin_placanja_update(request, pk):
    nacin = get_object_or_404(NacinPlacanja, pk=pk)

    if request.method == "POST":
        form = NacinPlacanjaForm(request.POST, instance=nacin)

        if form.is_valid():
            form.save()
            messages.success(request, "Način plaćanja je ažuriran.")
            return redirect("nacin_placanja_list")
    else:
        form = NacinPlacanjaForm(instance=nacin)

    return render(request, "sirana/form.html", {
        "form": form,
        "title": "Uredi način plaćanja",
    })


def nacin_placanja_delete(request, pk):
    nacin = get_object_or_404(NacinPlacanja, pk=pk)

    if request.method == "POST":
        nacin.delete()
        messages.success(request, "Način plaćanja je obrisan.")
        return redirect("nacin_placanja_list")

    return render(request, "sirana/confirm_delete.html", {
        "object": nacin,
    })


def sir_list(request):
    search = request.GET.get("search", "")

    sirevi = Sir.objects.all()

    if search:
        sirevi = sirevi.filter(naziv__icontains=search)

    return render(request, "sirana/sir_list.html", {
        "sirevi": sirevi,
        "search": search,
    })


def sir_create(request):
    if request.method == "POST":
        form = SirForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Sir je dodan.")
            return redirect("sir_list")
    else:
        form = SirForm()

    return render(request, "sirana/form.html", {
        "form": form,
        "title": "Dodaj sir",
    })


def sir_update(request, pk):
    sir = get_object_or_404(Sir, pk=pk)

    if request.method == "POST":
        form = SirForm(request.POST, instance=sir)

        if form.is_valid():
            form.save()
            messages.success(request, "Sir je ažuriran.")
            return redirect("sir_list")
    else:
        form = SirForm(instance=sir)

    return render(request, "sirana/form.html", {
        "form": form,
        "title": "Uredi sir",
    })


def sir_delete(request, pk):
    sir = get_object_or_404(Sir, pk=pk)

    if request.method == "POST":
        sir.delete()
        messages.success(request, "Sir je obrisan.")
        return redirect("sir_list")

    return render(request, "sirana/confirm_delete.html", {
        "object": sir,
    })



def narudzba_list(request):
    search = request.GET.get("search", "")

    narudzbe = Narudzba.objects.select_related("nacin_placanja").all()

    if search:
        if search.isdigit():
            narudzbe = narudzbe.filter(id=int(search))
        else:
            narudzbe = narudzbe.filter(naziv_kupca__icontains=search)

    return render(request, "sirana/narudzba_list.html", {
        "narudzbe": narudzbe,
        "search": search,
    })


def narudzba_create(request):
    sirevi = Sir.objects.all()

    if request.method == "POST":
        form = NarudzbaForm(request.POST)

        if form.is_valid():
            narudzba = form.save(commit = False)

            try:
                NarudzbaService.provjeri_aktivnost_placanja(narudzba)
                narudzba.save()

                sir_ids = request.POST.getlist("sir_id[]")
                kolicine = request.POST.getlist("kolicina_kg[]")
                cijene = request.POST.getlist("cijena_po_kg[]")
                popusti = request.POST.getlist("popust_postotak[]")

                for sir_id, kolicina, cijena, popust in zip(sir_ids, kolicine, cijene, popusti):
                    if sir_id and kolicina and cijena:
                        sir = Sir.objects.get(id=sir_id)

                        StavkaNarudzbe.objects.create(
                            narudzba=narudzba,
                            sir=sir,
                            kolicina_kg=Decimal(kolicina),
                            cijena_po_kg=Decimal(cijena),
                            popust_postotak=Decimal(popust or "0"),
                        )

                messages.success(request, "Narudžba je uspješno kreirana.")
                return redirect("narudzba_detail", pk=narudzba.pk)
            
            except ValidationError as e:
                form.add_error(None, e.message)

    else:
        form = NarudzbaForm()

    return render(request, "sirana/narudzba_create.html", {
        "form": form,
        "sirevi": sirevi,
        "title": "Dodaj narudžbu",
    })

def narudzba_detail(request, pk):
    narudzba = get_object_or_404(
        Narudzba.objects.select_related("nacin_placanja"),
        pk=pk
    )

    if request.method == "POST":
        form = NarudzbaForm(request.POST, instance=narudzba)

        try:
            NarudzbaService.provjeri_mogucnost_uredivanja(narudzba)

            if form.is_valid():
                form.save()
                messages.success(request, "Narudžba je spremljena.")
                return redirect("narudzba_detail", pk=narudzba.pk)
        
        except ValidationError as e:
            form.add_error(None, e.message)
    else:
        form = NarudzbaForm(instance=narudzba)

    stavke = narudzba.stavke.select_related("sir").all()
    sirevi = Sir.objects.all()

    return render(request, "sirana/narudzba_detail.html", {
        "narudzba": narudzba,
        "form": form,
        "stavke": stavke,
        "sirevi": sirevi,
        "ukupno": narudzba.ukupno(),
    })


def narudzba_delete(request, pk):
    narudzba = get_object_or_404(Narudzba, pk=pk)

    if request.method == "POST":
        narudzba.delete()
        messages.success(request, "Narudžba je obrisana.")
        return redirect("narudzba_list")

    return render(request, "sirana/confirm_delete.html", {
        "object": narudzba,
    })


def stavka_create(request, narudzba_id):
    narudzba = get_object_or_404(Narudzba, pk=narudzba_id)

    if request.method == "POST":
        sir_id = request.POST.get("sir_id")
        kolicina_kg = request.POST.get("kolicina_kg")
        cijena_po_kg = request.POST.get("cijena_po_kg")
        popust_postotak = request.POST.get("popust_postotak") or "0"

        if sir_id and kolicina_kg and cijena_po_kg:
            sir = get_object_or_404(Sir, pk=sir_id)

            StavkaNarudzbe.objects.create(
                narudzba=narudzba,
                sir=sir,
                kolicina_kg=Decimal(kolicina_kg),
                cijena_po_kg=Decimal(cijena_po_kg),
                popust_postotak=Decimal(popust_postotak),
            )

            messages.success(request, "Stavka je dodana u narudžbu.")
        else:
            messages.error(request, "Odaberi sir, količinu i cijenu.")

    return redirect("narudzba_detail", pk=narudzba.pk)



def stavka_update(request, pk):
    stavka = get_object_or_404(
        StavkaNarudzbe.objects.select_related("narudzba"),
        pk=pk
    )

    if request.method == "POST":
        form = StavkaNarudzbeForm(request.POST, instance=stavka)

        if form.is_valid():
            form.save()
            messages.success(request, "Stavka narudžbe je ažurirana.")
            return redirect("narudzba_detail", pk=stavka.narudzba.pk)
    else:
        form = StavkaNarudzbeForm(instance=stavka)

    return render(request, "sirana/stavka_form.html", {
        "form": form,
        "narudzba": stavka.narudzba,
        "title": "Uredi stavku narudžbe",
    })


def stavka_delete(request, pk):
    stavka = get_object_or_404(
        StavkaNarudzbe.objects.select_related("narudzba"),
        pk=pk
    )

    narudzba_id = stavka.narudzba.pk

    if request.method == "POST":
        stavka.delete()
        messages.success(request, "Stavka narudžbe je obrisana.")
        return redirect("narudzba_detail", pk=narudzba_id)

    return render(request, "sirana/confirm_delete.html", {
        "object": stavka,
    })