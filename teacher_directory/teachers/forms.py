from django import forms
from django.core.exceptions import ValidationError

from .models import Teacher


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = "__all__"

    def clean(self):
        categories = self.cleaned_data.get('subjects_taught')
        if categories and categories.count() > 5:
            raise ValidationError("Teachers can't teach more than five subjects")

        return self.cleaned_data


class BulkImportForm(forms.Form):
    file = forms.FileField()
