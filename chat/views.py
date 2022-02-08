from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Chat

@login_required
def index(request):
    chats = Chat.objects.filter(members=request.user)
    return render(request, 'chat/index.html',{'chats':chats})


@login_required
def room(request, room_name):
    chat = Chat.objects.get_or_create(name=room_name)[0]
    chat.members.add(request.user)
    return render(request, 'chat/room.html', {'room_name': room_name})
