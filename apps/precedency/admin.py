from django.contrib import admin

from . import models


@admin.register(models.Precedence)
class PrecedenceAdmin(admin.ModelAdmin):
    """Admin interface for Precedence model."""

    list_display = (
        "title",
        "created",
        "modified",
    )
    list_filter = (
        "created",
        "modified",
    )
    search_fields = (
        "title",
    )


@admin.register(models.UsersPrecedency)
class UsersPrecedencyAdmin(admin.ModelAdmin):
    """Admin interface for UsersPrecedency model."""

    list_display = (
        "precedence",
        "user",
        "attitude",
        "importance",
        "created",
        "modified",
    )
    list_filter = (
        "attitude",
        "importance",
        "created",
        "modified",
    )
