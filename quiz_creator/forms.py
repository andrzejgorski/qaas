from django import forms
from . import models
from django.core.validators import validate_email


class QuizForm(forms.ModelForm):
    class Meta:
        model = models.Quiz
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 10})
        }


class QuestionForm(forms.ModelForm):
    quiz = forms.IntegerField(widget=forms.HiddenInput()) 
    class Meta:
        model = models.Question
        fields = ['text']


class EmailForm(forms.Form):
    emails = forms.CharField(widget=forms.Textarea())

    @classmethod
    def sanitize(cls, text):
        return (
            element.strip() for element in text.split(',')
        )

    def is_valid(self):
        result = super().is_valid()
        if not result:
            return result
        
        try:
            for text in self.sanitize(self.data['emails']):
                validate_email(text)
        except ValidationError:
            return False
        return True


ChoiceFormset = forms.inlineformset_factory(models.Question, models.Choice, fields=('text', 'correct'))
