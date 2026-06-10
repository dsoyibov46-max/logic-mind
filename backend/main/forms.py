from django import forms
from django.contrib.auth import get_user_model
from .models import ClassGroup
from .models import ClassGroup, Assignment
User = get_user_model()


class ClassGroupForm(forms.ModelForm):
    students = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(role='student'),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="O‘quvchilar"
    )

    class Meta:
        model = ClassGroup
        fields = ['name', 'description', 'students']
        labels = {
            'name': 'Guruh nomi',
            'description': 'Guruh haqida',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masalan: 10-A sinf'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Guruh haqida qisqacha yozing',
                'rows': 4
            }),
        }
class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'group', 'due_date', 'max_score', 'status']
        labels = {
            'title': 'Topshiriq nomi',
            'description': 'Topshiriq tavsifi',
            'group': 'Guruh',
            'due_date': 'Topshiriq muddati',
            'max_score': 'Maksimal ball',
            'status': 'Holati',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masalan: Mantiqiy test №1'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Topshiriq shartini yozing...',
                'rows': 5
            }),
            'due_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'max_score': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 100
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'group': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        super().__init__(*args, **kwargs)

        if teacher:
            self.fields['group'].queryset = ClassGroup.objects.filter(teacher=teacher)