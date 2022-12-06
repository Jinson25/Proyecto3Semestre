from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Escribe tu titulo de la tarea'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Escribe tu descripcion de la tarea'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input m-auto'}),
        }