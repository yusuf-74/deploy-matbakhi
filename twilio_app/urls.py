from django.urls import path
from .views import Send
urlpatterns = [
    path('', Send.as_view()),
]

