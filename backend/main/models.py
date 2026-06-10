from django.db import models
from django.conf import settings
from django.db import models


class ClassGroup(models.Model):
    name = models.CharField(max_length=150)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='teaching_groups'
    )
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='student_groups',
        blank=True
    )
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Class Group"
        verbose_name_plural = "Class Groups"
        ordering = ['-created_at']

    def __str__(self):
        return self.name
class Assignment(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('closed', 'Closed'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    group = models.ForeignKey(
        ClassGroup,
        on_delete=models.CASCADE,
        related_name='assignments'
    )
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_assignments'
    )
    due_date = models.DateTimeField(blank=True, null=True)
    max_score = models.PositiveIntegerField(default=100)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='published'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Assignment"
        verbose_name_plural = "Assignments"
        ordering = ['-created_at']

    def __str__(self):
        return self.title