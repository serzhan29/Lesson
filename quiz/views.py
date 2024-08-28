from django.shortcuts import render, get_object_or_404, redirect
from .models import Quiz, Question, Answer, UserQuizResult
from django.contrib.auth.decorators import login_required
from main.models import Lesson

def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz/quiz_list.html', {'quizzes': quizzes})


@login_required
def quiz_detail(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    questions = quiz.questions.all()

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

        return redirect('quiz:quiz_result', pk=quiz.pk, score=score)

    return render(request, 'quiz/quiz_detail.html', {'quiz': quiz, 'questions': questions})


@login_required
def quiz_result(request, quiz_id):
    # Получение теста по идентификатору
    quiz = get_object_or_404(Quiz, id=quiz_id)

    # Получение результатов теста для текущего пользователя
    result = get_object_or_404(UserQuizResult, quiz=quiz, user=request.user)

    # Получение списка всех результатов пользователя
    results = UserQuizResult.objects.filter(user=request.user).order_by('-date_taken')

    # Подготовка данных для шаблона
    user_answers = {question.id: result.answers.filter(question=question).values_list('id', flat=True) for question in
                    quiz.questions.all()}

    context = {
        'quiz': quiz,
        'result': result,
        'results': results,
        'user_answers': user_answers,
    }
    return render(request, 'quiz/result.html', context)
