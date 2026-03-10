# portfolio/serializers.py

from rest_framework import serializers
from .models import About, Skill, Project, ContactMessage


class AboutSerializer(serializers.ModelSerializer):
    """
    Serializes personal info. profile_picture_url and
    cv_url gives React the full download link for the CV file.
    """
    cv_url = serializers.SerializerMethodField()
    profile_picture_url = serializers.SerializerMethodField()

    class Meta:
        model = About
        fields = [
            'id', 'name', 'title', 'bio',
            'profile_picture_url', 'cv_url',
            'email', 'github', 'linkedin',
            'twitter', 'location',
        ]

    def get_cv_url(self, obj):
        request = self.context.get('request')
        if obj.cv and request:
            return request.build_absolute_uri(obj.cv.url)
        return None

    def get_profile_picture_url(self, obj):
        request = self.context.get('request')
        if obj.profile_picture and obj.profile_picture.name and request:
            return request.build_absolute_uri(obj.profile_picture.url)
        return None


class SkillSerializer(serializers.ModelSerializer):
    
    category_display = serializers.CharField(
        source='get_category_display', read_only=True
    )

    class Meta:
        model = Skill
        fields = [
            'id', 'name', 'category',
            'category_display', 'proficiency',
            'icon', 'order',
        ]


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializes projects. tech_stack_list splits the
    comma-separated string into a clean array for React.
    """
    category_display = serializers.CharField(
        source='get_category_display', read_only=True
    )
    image_url = serializers.SerializerMethodField()
    tech_stack_list = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description',
            'category', 'category_display',
            'tech_stack', 'tech_stack_list',
            'image_url', 'github_url', 'live_url',
            'is_featured', 'created_at', 'order',
        ]

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

    def get_tech_stack_list(self, obj):
        # Converts "Django, React, PostgreSQL" → ["Django", "React", "PostgreSQL"]
        if obj.tech_stack:
            return [tech.strip() for tech in obj.tech_stack.split(',')]
        return []


class ContactMessageSerializer(serializers.ModelSerializer):
    """
    Handles incoming contact form submissions.
    Read-only fields prevent tampering via the API.
    """
    class Meta:
        model = ContactMessage
        fields = [
            'id', 'name', 'email',
            'mobile_number', 'message', 'sent_at',
        ]
        read_only_fields = ['id', 'sent_at']

    def validate_mobile_number(self, value):
        """
        Basic validation — must be at least 10 digits.
        """
        digits = ''.join(filter(str.isdigit, value))
        if len(digits) < 10:
            raise serializers.ValidationError(
                "Enter a valid mobile number (at least 10 digits)."
            )
        return value

    def validate_message(self, value):
        """
        Message must have some real content.
        """
        if len(value.strip()) < 10:
            raise serializers.ValidationError(
                "Message is too short. Please write at least 10 characters."
            )
        return value