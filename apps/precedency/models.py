from django.contrib.postgres.fields import CICharField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class Precedence(BaseModel):
    """Life precedence."""

    title = CICharField(
        verbose_name=_("title"),
        max_length=65,
        unique=True
    )

    def __str__(self):
        # pylint: disable=invalid-str-returned
        return self.title

    class Meta:
        verbose_name = _("Precedency")
        verbose_name_plural = _("Precedence")


class UsersPrecedency(BaseModel):
    """User life precedence with its attitude and importance."""

    ATTITUDES = (
        (1, _("Negative")),
        (2, _("Positive")),
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
        validators=[MinValueValidator(1), MaxValueValidator(2)],
        choices=ATTITUDES,
        db_index=True
    )
    importance = models.PositiveSmallIntegerField(
        verbose_name=_("importance"),
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    def __str__(self) -> str:
        return f"{self.user} precedency"

    class Meta:
        unique_together = (("precedency", "user"),)
        verbose_name = _("Users precedency")
        verbose_name_plural = _("Users precedence")
