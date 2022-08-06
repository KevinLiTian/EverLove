""" Views """
from django.shortcuts import render


def lobby(request):
    """ Chat Lobby """
    return render(request, 'chat/lobby.html', {
        'roomID': 'Test'
    })
