from django.urls import path
from .views import UserProfile,UserMessage,CreateNewMessage

urlpatterns = [
    path("friends/",UserProfile.as_view({"post":"list"})),
    path("messages/",UserMessage.as_view({'post': 'list'})),
    path("new/message/",CreateNewMessage.as_view({'post': 'list'}))

]
