from django.shortcuts import render, get_object_or_404, redirect
from .models import Quiz, Question, Answer, UserQuizResult
from django.contrib.auth.decorators import login_required
from main.models import Lesson
from django.utils import timezone
from .forms import AnswerForm

@login_required
def quiz_list(request):
    quizzes = Quiz.objects.all()
    user = request.user

    # Получаем идентификаторы завершенных викторин
    completed_quiz_ids = UserQuizResult.objects.filter(user=user).values_list('quiz_id', flat=True)

    return render(request, 'quiz/quiz_list.html', {
        'quizzes': quizzes,
        'completed_quiz_ids': completed_quiz_ids,
    })


@login_required
def quiz_detail(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    questions = quiz.questions.all()

    # Проверяем, сдавал ли пользователь этот тест ранее
    if UserQuizResult.objects.filter(user=request.user, quiz=quiz).exists():
        return redirect('quiz:quiz_result', quiz_id=quiz.pk)

    if request.method == 'POST':
        total_questions = questions.count()
        correct_answers = 0

        # Проверка выбранных ответов
        for question in questions:
            selected_answers = request.POST.getlist(f'question_{question.id}')
            correct_answers += sum(1 for answer in question.answers.filter(is_correct=True) if str(answer.id) in selected_answers)

        score = (correct_answers / total_questions) * 100

        # Сохранение результата теста
        UserQuizResult.objects.create(
            user=request.user,
            quiz=quiz,
            score=score,
            completed_at=timezone.now(),
        )

        return redirect('quiz:quiz_result', quiz_id=quiz.pk)

    return render(request, 'quiz/quiz_detail.html', {'quiz': quiz, 'questions': questions})



@login_required
def quiz_result(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    user = request.user
    result = get_object_or_404(UserQuizResult, quiz=quiz, user=user)

    # Получаем ответы пользователя
    user_answers = {}
    for question in quiz.questions.all():
        answers = request.POST.getlist(f'question_{question.id}')
        user_answers[question.id] = [int(answer_id) for answer_id in answers]

    # Подсчитываем количество правильных ответов
    correct_answers_count = 0
    for question in quiz.questions.all():
        correct_answers = set(answer.id for answer in question.answers.filter(is_correct=True))
        if set(user_answers.get(question.id, [])) == correct_answers:
            correct_answers_count += 1

    context = {
        'quiz': quiz,
        'result': result,
        'user_answers': user_answers,
        'correct_answers_count': correct_answers_count,
    }
    return render(request, 'quiz/result.html', context)


def take_quiz(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    questions = quiz.questions.all()

    if request.method == 'POST':
        form = AnswerForm(request.POST, questions=questions)
        if form.is_valid():
            score = 0
            for question in questions:
                if question.question_type == 'text':
                    user_answer = form.cleaned_data[f'question_{question.id}']
                    correct_answers = question.answers.filter(is_correct=True)
                    # Проверка правильности ответа (упрощенный пример)
                    if user_answer in [ans.text for ans in correct_answers]:
                        score += 1
                elif question.question_type == 'table':
                    # Логика для проверки таблицы
                    table_answer_1 = form.cleaned_data[f'table_row1_{question.id}']
                    table_answer_2 = form.cleaned_data[f'table_row2_{question.id}']
                    # Здесь можно проверять правильность заполнения таблицы
                elif question.question_type == 'reorder':
                    # Логика для перестановки
                    user_reorder = form.cleaned_data[f'reorder_{question.id}']
                    # Проверяем перестановку с правильным порядком

            # Сохраняем результат
            UserQuizResult.objects.create(
                user=request.user,
                quiz=quiz,
                score=score,
                completed_at=timezone.now()
            )
            return redirect('quiz_result', quiz_id=quiz.id)
    else:
        form = AnswerForm(questions=questions)

    return render(request, 'take_quiz.html', {'quiz': quiz, 'form': form})




