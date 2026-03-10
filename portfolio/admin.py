# portfolio/admin.py

from django.contrib import admin
from .models import About, Skill, Project, ContactMessage


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'email', 'location']


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency', 'order']
    list_filter = ['category']
    list_editable = ['order', 'proficiency']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_featured', 'order']
    list_filter = ['category', 'is_featured']
    list_editable = ['is_featured', 'order']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'mobile_number', 'sent_at', 'is_read']
    list_filter = ['is_read']
    list_editable = ['is_read']
    readonly_fields = ['name', 'email', 'mobile_number', 'message', 'sent_at']


    