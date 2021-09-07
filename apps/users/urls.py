from django.urls import path

from . import views

urlpatterns = [
    path(
        "activate/<uid64>/<token>/",
        views.ActivateAccountView.as_view(),
        name="activate-account",
    )
]
