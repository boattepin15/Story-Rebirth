from django.urls import path
from app.views import HomeView
urlpatterns = [
    path('', view=HomeView.as_view(), name="home")
]
