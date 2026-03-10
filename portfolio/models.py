# portfolio/models.py

from django.db import models


class About(models.Model):
    """
    Stores Personal Information for the "About Me" section of the portfolio.
    """
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=150)          # e.g. "BBIT Student & Software Developer"
    bio = models.TextField()                           # Your full bio/about me
    profile_picture = models.ImageField(
        upload_to='profile/', blank=True, null=True
    )
    cv = models.FileField(
        upload_to='cv/', blank=True, null=True        # CV PDF uploaded via Django admin
    )
    email = models.EmailField()
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    location = models.CharField(max_length=100, default='Nairobi, Kenya')

    class Meta:
        verbose_name = 'About'
        verbose_name_plural = 'About'

    def __str__(self):
        return self.name


class Skill(models.Model):
    """
    Technical skills — grouped by category.
    """
    CATEGORY_CHOICES = [
        ('backend', 'Backend Development'),
        ('frontend', 'Frontend Development'),
        ('cybersecurity', 'Cybersecurity'),
        ('database', 'Database'),
        ('tools', 'Tools & DevOps'),
    ]

    name = models.CharField(max_length=100)           # e.g. "Django", "React", "Kali Linux"
    category = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES
    )
    proficiency = models.IntegerField(
        default=80,                                    # Percentage 0-100
        help_text='Skill level as a percentage (0-100)'
    )
    icon = models.CharField(
        max_length=100, blank=True,                   # e.g. CSS class or icon name
        help_text='Icon class name e.g. devicon-python-plain'
    )
    order = models.IntegerField(default=0)            # Controls display order

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class Project(models.Model):
    """
    Portfolio projects — both software dev and cybersecurity.
    """
    CATEGORY_CHOICES = [
        ('software', 'Software Development'),
        ('cybersecurity', 'Cybersecurity'),
        ('fullstack', 'Full Stack'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES, default='software'
    )
    tech_stack = models.CharField(
        max_length=300,
        help_text='Comma-separated list e.g. Django, React, PostgreSQL'
    )
    image = models.ImageField(
        upload_to='projects/', blank=True, null=True
    )
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)  # Show on homepage
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    """
    Messages sent through your portfolio's contact form.
    Stores sender details so you can reply via email.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=20)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)      # Track which messages you've seen

    class Meta:
        ordering = ['-sent_at']

    def __str__(self):
        return f"Message from {self.name} ({self.email}) - {self.sent_at.strftime('%d %b %Y')}"