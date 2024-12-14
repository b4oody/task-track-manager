def http_referer(request):
    return {"referer": request.META.get("HTTP_REFERER", "/")}
