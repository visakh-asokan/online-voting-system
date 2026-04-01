from django.urls import path
from . import views
from django.contrib.auth.views import PasswordChangeView

urlpatterns = [
    path('', views.home, name='home'),

    # Voting
    path('vote/<int:election_id>/', views.vote, name='vote'),
    path('results/<int:election_id>/', views.results, name='results'),

    # Auth
    path('register/', views.register, name='register'),
    path('logout/', views.custom_logout, name='logout'),

    # User features
    path('change-password/', PasswordChangeView.as_view(
        template_name='change_password.html',
        success_url='/'
    ), name='change_password'),

    # Admin features
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('create-election/', views.create_election, name='create_election'),
    path('add-candidate/<int:election_id>/', views.add_candidate, name='add_candidate'),
    path('delete-candidate/<int:candidate_id>/', views.delete_candidate, name='delete_candidate'),
    path('stop-voting/<int:election_id>/', views.stop_voting, name='stop_voting'),
    path('delete-election/<int:election_id>/', views.delete_election, name='delete_election'),
]