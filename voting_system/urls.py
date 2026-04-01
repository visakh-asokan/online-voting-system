from django.contrib import admin
from django.urls import path, include
from voting import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('voting.urls')),
    path('login/', views.CustomLoginView.as_view(), name='login'),
]