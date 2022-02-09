import re
from django.shortcuts import render
from django.http import JsonResponse
import random
import time
from agora_token_builder import RtcTokenBuilder
import json
from .models import RoomMember

from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def lobby(request):
    return render(request, "base/lobby.html")

def room(request):
    return render(request, "base/room.html")

def get_token(request):

    appId = '582c9a152d9c4fcc92659d3d5d962f6c'

    appCertificate = '46bfd084b52e4d92bf532c6ac6a10ec9'
    channelName = request.GET.get('channel')
    uid = random.randint(1,230)
    role = 1

    expirationTimeInSeconds = 3600
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

    return JsonResponse({'token':token, 'uid': uid },safe=False)

@csrf_exempt
def createMember(request):
    data  = json.loads(request.body)

    member, created = RoomMember.objects.get_or_create(
        username = data['name'],
        uid = data['UID'],
        room_name = data['room_name'],
    )
    return JsonResponse({'name':data['name']},safe=False)


def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(
        uid = uid,
        room_name = room_name,
    )

    username = member.username
    return JsonResponse({'name':member.username},safe=False)

@csrf_exempt
def deleteMember(request):
    data  = json.loads(request.body)

    member = RoomMember.objects.get(
        username = data['name'],
        uid = data['UID'],
        room_name = data['room_name'],
    )
    member.delete()
    return JsonResponse({'message':"Member deleted"},safe=False)
