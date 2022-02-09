from django.urls import path

from .views import lobby,room, get_token, createMember, getMember, deleteMember 

urlpatterns = [
    path("",lobby),
    path('room/',room),
    path('get_token/', get_token),
    path('create_member/', createMember),
    path('get_member/', getMember),
    path('delete_member/', deleteMember),

]