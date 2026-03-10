# portfolio/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings

from .models import About, Skill, Project, ContactMessage
from .serializers import (
    AboutSerializer, SkillSerializer,
    ProjectSerializer, ContactMessageSerializer,
)


class AboutView(APIView):
    """
    GET /api/about/
    Returns Vincent's personal info — bio, CV link, social links.
    """
    def get(self, request):
        # We only ever have one About record
        about = About.objects.first()
        if not about:
            return Response(
                {'error': 'Profile not set up yet.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = AboutSerializer(about, context={'request': request})
        return Response(serializer.data)


class SkillListView(APIView):
    """
    GET /api/skills/
    Returns all skills, grouped by category for easy use in React.
    """
    def get(self, request):
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)

        # Group skills by category so React can render them in sections
        grouped = {}
        for skill in serializer.data:
            cat = skill['category_display']
            if cat not in grouped:
                grouped[cat] = []
            grouped[cat].append(skill)

        return Response({
            'skills': serializer.data,        # flat list
            'grouped': grouped,               # grouped by category
        })


class ProjectListView(APIView):
    """
    GET /api/projects/           → all projects
    GET /api/projects/?featured  → only featured projects
    GET /api/projects/?category=cybersecurity  → filter by category
    """
    def get(self, request):
        projects = Project.objects.all()

        # Optional filters via query params
        if 'featured' in request.query_params:
            projects = projects.filter(is_featured=True)

        category = request.query_params.get('category')
        if category:
            projects = projects.filter(category=category)

        serializer = ProjectSerializer(
            projects, many=True, context={'request': request}
        )
        return Response(serializer.data)


class ProjectDetailView(APIView):
    """
    GET /api/projects/<id>/
    Returns a single project by its ID.
    """
    def get(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response(
                {'error': 'Project not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProjectSerializer(project, context={'request': request})
        return Response(serializer.data)


class ContactView(APIView):
    """
    POST /api/contact/
    Receives contact form data, saves to database,
    and sends Vincent an email notification.
    """
    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)

        if serializer.is_valid():
            # Save the message to the database
            contact = serializer.save()

            # Send email notification to Vincent (optional but professional)
            try:
                send_mail(
                    subject=f"📬 New Portfolio Message from {contact.name}",
                    message=(
                        f"Name: {contact.name}\n"
                        f"Email: {contact.email}\n"
                        f"Mobile: {contact.mobile_number}\n\n"
                        f"Message:\n{contact.message}"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_RECIPIENT_EMAIL],
                    fail_silently=True,   # Don't crash if email fails
                )
            except Exception:
                pass  # Email failure shouldn't break the API response

            return Response(
                {
                    'success': True,
                    'message': (
                        f"Thank you {contact.name}! "
                        "Your message has been received. "
                        "Vincent will get back to you soon."
                    )
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {'success': False, 'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


class StatsView(APIView):
    """
    GET /api/stats/
    Returns portfolio summary numbers for a stats section in React.
    """
    def get(self, request):
        return Response({
            'total_projects': Project.objects.count(),
            'featured_projects': Project.objects.filter(is_featured=True).count(),
            'total_skills': Skill.objects.count(),
            'cybersecurity_projects': Project.objects.filter(
                category='cybersecurity'
            ).count(),
        })