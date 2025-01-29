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

class AssignCourseForm(forms.Form):
    courses = forms.ModelMultipleChoiceField(
        queryset=models.Course.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

class TrainerEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = models.TrainerUser
        fields = ['phone_number', 'about_me']
        widgets = {
            'about_me': forms.Textarea(attrs={'rows': 4}),
        }
