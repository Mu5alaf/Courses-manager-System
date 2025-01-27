from django import forms
from . import models


class CourseForm(forms.ModelForm):
    class Meta:
        model = models.Course
        fields = [
            'title',
            'description',
            'image',
            'video',
            'price_type',
            'price',
            'total_hours',
            'created_by',
        ]
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            raise forms.ValidationError("Please upload an image.")
        return image
