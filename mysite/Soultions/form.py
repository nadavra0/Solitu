from django import forms
from .models import *
from django.core.validators import FileExtensionValidator


class QustionForm (forms.Form):
    quiz = forms.FileField(
        label="File:",
        validators = [FileExtensionValidator(allowed_extensions=["txt"])]
    )

    unsloved = forms.FileField(
        label="Unsloved:",
        validators = [FileExtensionValidator(allowed_extensions=["txt"])]

    )


