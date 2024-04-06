from django.shortcuts import render


# 4dev
def index(request):
    return render(request, "chat/index.html")


# 4dev
def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})
