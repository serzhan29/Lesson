from django.shortcuts import render, get_object_or_404, redirect
from .models import Quiz, Question, Answer, UserQuizResult
from django.contrib.auth.decorators import login_required
from main.models import Lesson
from django.utils import timezone


def quiz_list(request):
    quizzes = Quiz.objects.all()
    user = request.user
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

        for question in questions:
            selected_answers = request.POST.getlist(str(question.id))
            correct_answers += sum(1 for answer in question.answers.filter(is_correct=True) if str(answer.id) in selected_answers)

        score = (correct_answers / total_questions) * 100

        UserQuizResult.objects.create(
            user=request.user,
            quiz=quiz,
            score=score,
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




