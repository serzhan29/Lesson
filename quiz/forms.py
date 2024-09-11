from django import forms
from .models import Question, Answer

class AnswerForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super().__init__(*args, **kwargs)

        for question in questions:
            if question.question_type == 'text':
                self.fields[f'question_{question.id}'] = forms.CharField(
                    label=question.text, widget=forms.TextInput(attrs={'class': 'form-control'})
                )
            elif question.question_type == 'table':
                # Добавим отдельные поля для заполнения ячеек таблицы
                self.fields[f'table_row1_{question.id}'] = forms.CharField(
                    label=f'{question.text} - Ряд 1, Колонка 1', widget=forms.TextInput(attrs={'class': 'form-control'})
                )
                self.fields[f'table_row2_{question.id}'] = forms.CharField(
                    label=f'{question.text} - Ряд 1, Колонка 2', widget=forms.TextInput(attrs={'class': 'form-control'})
                )
                # Добавляй другие ряды, если необходимо
            elif question.question_type == 'reorder':
                self.fields[f'reorder_{question.id}'] = forms.CharField(
                    label=question.text, widget=forms.HiddenInput()
                )
                # Логика для перестановки обрабатывается через JS
