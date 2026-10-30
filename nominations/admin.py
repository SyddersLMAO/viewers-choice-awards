
from django.contrib import admin
from django.db.models import Count

from .models import Category, Nomination


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'nomination_count',
        'is_active',
        'created_at',
    )
    list_filter = ('is_active',)
    search_fields = ('name',)
    ordering = ('name',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(
            total_nominations=Count('nominations')
        )

    @admin.display(description='Nominations', ordering='total_nominations')
    def nomination_count(self, obj):
        return obj.total_nominations


@admin.register(Nomination)
class NominationAdmin(admin.ModelAdmin):
    list_display = (
        'nominee_name',
        'category',
        'submitter_email',
        'submitted_at',
    )
    list_filter = (
        'category',
        'submitted_at',
    )
    search_fields = (
        'nominee_name',
        'submitter_email',
    )
    readonly_fields = ('submitted_at',)
    date_hierarchy = 'submitted_at'
    ordering = ('-submitted_at',)
    list_per_page = 50
