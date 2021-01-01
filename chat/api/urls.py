from django.urls import path
from .views import UserProfile,UserMessage,CreateNewMessage,LoginUser,UserCreateView

urlpatterns = [
    path('singup/',UserCreateView.as_view()),
    path("login/",LoginUser.as_view({"post":"login"})),
    path("friends/",UserProfile.as_view({"post":"list"})),
    path("messages/",UserMessage.as_view({'post': 'list'})),
    path("new/message/",CreateNewMessage.as_view({'post': 'list'}))

]
