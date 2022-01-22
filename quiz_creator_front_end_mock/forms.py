from quiz_creator import forms


class QuestionForm(forms.QuestionForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].label = 'Question'


ChoiceFormset = forms.ChoiceFormset
EmailForm = forms.EmailForm
