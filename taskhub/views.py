
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def get_index_page(request: HttpRequest) -> HttpResponse:
    return render(request, "index/index.html")
