from django.urls import path, re_path
from electoral import views

urlpatterns = [
    # The home page
    path('voting/', views.voting_page, name='voting'),
]
