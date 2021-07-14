from django.shortcuts import render


def index(request):
    return render(request, 'chat/index.html', {})

def rand_int(request):
    return render(request, 'chat/randint.html', {
        'text': "Hello, WebScket"
    })

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })
