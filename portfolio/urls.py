# portfolio/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # About / Profile
    path('about/', views.AboutView.as_view(), name='about'),

    # Skills
    path('skills/', views.SkillListView.as_view(), name='skills'),

    # Projects
    path('projects/', views.ProjectListView.as_view(), name='projects'),
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name='project-detail'),

    # Contact form
    path('contact/', views.ContactView.as_view(), name='contact'),

    # Stats
    path('stats/', views.StatsView.as_view(), name='stats'),
]