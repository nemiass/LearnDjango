from django.http import HttpRequest, HttpResponse

# Utilities
from datetime import datetime
import json


def hello_world(request: HttpRequest) -> HttpResponse:
    now = datetime.now().strftime("%b %dth, %Y - %H:%M hrs")
    return HttpResponse(f"Hola mundo: {now}")


def sort_integers(request: HttpRequest):
    # ejemplo recibiendo query Strings
    list_str_numbers = request.GET["numbers"].split(",")
    list_numbers = [int(n) for n in list_str_numbers]
    list_numbers.sort()
    data = {
        "status": "ok",
        "numbers": list_numbers,
        "message": "Integers sorted successfuly",
    }
    return HttpResponse(json.dumps(data, indent=4), content_type="application/json")


def say_hi(request: HttpRequest, name: str, age: int):
    if age < 12:
        message = f"Sorry {name}, you are not allowed here"
    else:
        message = f"Hello, {name}!, Welcome to Fakegram"
    return HttpResponse(message)
