from django import forms
from .models import StudentSubmission, StudentAnswer, Question

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = StudentSubmission
        fields = ['assignment']

    def __init__(self, *args, **kwargs):
        assignment = kwargs.pop('assignment', None)
        super().__init__(*args, **kwargs)
        if assignment:
            questions = assignment.questions.all()
            for question in questions:
                field_name = f"question_{question.id}"
                if question.question_type == Question.TEXT:
                    self.fields[field_name] = forms.CharField(label=question.question_text, widget=forms.Textarea)
                elif question.question_type == Question.CHOICE:
                    choices = [(answer.id, answer.answer_text) for answer in question.answers.all()]
                    self.fields[field_name] = forms.ChoiceField(label=question.question_text, choices=choices)
                elif question.question_type == Question.MULTICHOICE:
                    choices = [(answer.id, answer.answer_text) for answer in question.answers.all()]
                    self.fields[field_name] = forms.MultipleChoiceField(label=question.question_text, choices=choices, widget=forms.CheckboxSelectMultiple)
