from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Nomination(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='nominations'
    )
    nominee_name = models.CharField(max_length=150)
    nominee_platform = models.CharField(max_length=100, blank=True)
    nominee_url = models.URLField(blank=True)
    reason = models.TextField()
    submitted_by = models.CharField(max_length=100)
    submitter_email = models.EmailField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f'{self.nominee_name} — {self.category.name}'