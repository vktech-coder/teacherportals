from django import forms
from .models import Student

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

# class StudentForm(forms.ModelForm):
#     class Meta:
#         model = Student
#         fields = ['name', 'subject', 'marks']

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'subject', 'marks']

    # def clean(self):
    #     cleaned_data = super().clean()
    #     name = cleaned_data.get('name')
    #     subject = cleaned_data.get('subject')

    #     # 🔥 Allow update if it already exists (skip uniqueness check)
    #     if name and subject:
    #         existing = Student.objects.filter(name=name, subject=subject).first()
    #         if existing and self.instance.pk != existing.pk:
    #             # If it already exists and not the same instance, we skip raising error
    #             self.instance = existing  # overwrite instance
    #     return cleaned_data