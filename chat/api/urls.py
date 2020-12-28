from django.urls import path
from .views import UserProfile,UserMessage

urlpatterns = [
    path("friend/<id>/list/",UserProfile.as_view({"get":"list"})),
    path("message/<id_s>/<id_r>/",UserMessage.as_view({'get': 'list'}))
]
