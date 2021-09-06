from django.contrib.postgres.fields import CICharField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class Precedence(BaseModel):
    """Life precedence."""

    title = CICharField(
        verbose_name=_("title"),
        max_length=65
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Precedency")
        verbose_name_plural = _("Precedence")


class UsersPrecedency(BaseModel):
    """User life precedence with its attitude and importance."""

    ATTITUDES = (
        (0, _("Negative")),
        (1, _("Positive")),
    )

    precedency = models.ForeignKey(
        verbose_name=_("precedency"),
        to="precedency.Precedence",
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        verbose_name=_("user"),
        to="users.user",
        on_delete=models.CASCADE
    )
    attitude = models.PositiveSmallIntegerField(
        verbose_name=_("attitude"),
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        choices=ATTITUDES
    )
    importance = models.PositiveSmallIntegerField(
        verbose_name=_("importance"),
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    def __str__(self) -> str:
        return f"{self.user}| {self.precedency.title}"

    class Meta:
        verbose_name = _("Users precedency")
        verbose_name_plural = _("Users precedence")
