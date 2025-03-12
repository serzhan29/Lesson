from .models import Quiz, Question, Answer, UserQuizResult, Points
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import AnswerForm
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings


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
    detailed_answers = []  # Список для хранения деталей ответов
    for question in quiz.questions.all():
        correct_answers = set(answer.id for answer in question.answers.filter(is_correct=True))
        user_selected_answers = set(user_answers.get(question.id, []))

        # Подготовим тексты ответов пользователя
        user_answers_text = []
        if user_selected_answers:
            user_answers_text = [answer.text for answer in question.answers.filter(id__in=user_selected_answers)]

        # Добавляем информацию о вопросе и ответах
        detailed_answers.append({
            'question': question,
            'user_answers': user_selected_answers,
            'user_answers_text': user_answers_text,  # Добавляем текст выбранных ответов
            'correct_answers': correct_answers,
            'is_correct': user_selected_answers == correct_answers,
        })

        if user_selected_answers == correct_answers:
            correct_answers_count += 1

    context = {
        'quiz': quiz,
        'result': result,
        'user_answers': user_answers,
        'correct_answers_count': correct_answers_count,
        'detailed_answers': detailed_answers,  # Добавляем детализированные ответы
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


#===============================MultuAnswer TEST ==============================================

def test_success(request):
    return render(request, 'test/test_success.html')


# Страница с отображением всех тестов
def test_list(request):
    tests = Tests.objects.all()
    return render(request, 'test/test_list.html', {'tests': tests})


from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .models import Tests, MultyTest, TestResponse2

@login_required
def test_detail(request, test_id):
    # Получаем тест или возвращаем 404
    test = get_object_or_404(Tests, id=test_id)

    # Проверяем, сдавал ли пользователь тест
    if TestResponse2.objects.filter(student=request.user, test=test).exists():
        # Если уже сдавал, перенаправляем на страницу благодарности
        return redirect('quiz:test_success')

    # Получаем все вопросы теста
    multy_tests = test.tests.all()

    # Подготавливаем данные вопросов и ответов
    questions_and_answers = []
    for multy_test in multy_tests:
        answers = multy_test.answers.all()
        questions_and_answers.append({
            'question': multy_test,
            'answers': answers
        })

    if request.method == 'POST':
        # Обрабатываем ответы
        for multy_test in multy_tests:
            # Получаем ответы на текущий вопрос
            answers = request.POST.getlist(f'answer_text_{multy_test.id}')
            if answers:
                # Создаем отдельную запись для каждого вопроса
                TestResponse2.objects.create(
                    student=request.user,
                    test=test,
                    multy_test=multy_test,
                    response_data=answers  # Сохраняем ответы как JSON
                )

        # Перенаправляем на страницу благодарности
        return redirect('quiz:test_success')

    return render(request, 'test/test_detail.html', {
        'test': test,
        'questions_and_answers': questions_and_answers
    })


@login_required
def all_student_responses(request):
    # Получаем все ответы студентов для всех тестов и группируем их по студенту и тесту
    responses = TestResponse2.objects.all().select_related('student', 'test').order_by('student', 'test')

    score_2 = Points.objects.all()

    # Создаем словарь для группировки ответов по студентам
    student_responses = {}
    for response in responses:
        if response.student not in student_responses:
            student_responses[response.student] = {}

        if response.test not in student_responses[response.student]:
            student_responses[response.student][response.test] = {
                'responses': [],  # Список ответов
                'score': None,  # Здесь будет оценка
            }

        # Добавляем ответ к соответствующему студенту и тесту
        student_responses[response.student][response.test]['responses'].append(response)

    # Получаем все вопросы (MultyTest) для отображения
    questions = MultyTest.objects.all()

    # Теперь добавляем информацию о баллах (оценках) для каждого студента и теста
    for student in student_responses:
        for test in student_responses[student]:
            # Получаем оценку для студента и теста
            score = Points.objects.filter(user=student, test=test).first()
            # Если оценка существует, сохраняем её в словарь
            if score:
                student_responses[student][test]['score'] = score.score  # Сохраняем только оценку
            else:
                student_responses[student][test]['score'] = None  # Если оценки нет, то сохраняем None

    # Если запрос POST (т.е. форма отправлена)
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        test_id = request.POST.get('test_id')
        score_value = request.POST.get('score')

        student = request.user.__class__.objects.get(id=student_id)  # Получаем студента
        test = Tests.objects.get(id=test_id)  # Получаем тест

        # Получаем существующую оценку для этого студента и теста
        existing_score = Points.objects.filter(user=student, test=test).first()

        if existing_score:
            # Если оценка существует, обновляем её
            existing_score.score = score_value
            existing_score.save()
            messages.success(request, "Оценка успешно обновлена.")
        else:
            # Если оценки нет, создаем новую
            Points.objects.create(user=student, test=test, score=score_value)
            messages.success(request, "Оценка успешно добавлена.")

        # После обновления/добавления оценки перенаправляем на ту же страницу
        return redirect('quiz:all_student_responses')  # Можно использовать название пути, как у вас в urls

    return render(request, 'test/all_student_responses.html', {
        'student_responses': student_responses,
        'questions': questions,
        'score_2': score_2,
    })

@login_required
@require_POST
def add_or_update_score(request):
    # Получаем ID теста и оценку из POST-запроса
    test_id = request.POST.get('test_id')
    score = request.POST.get('score')

    # Логируем данные для отладки
    print(f"DEBUG: test_id={test_id}, score={score}")

    # Получаем текущего пользователя (студента)
    student = request.user

    if test_id and score:
        # Проверка, является ли строка числом и положительным целым числом
        if score.isdigit() and int(score) > 0:
            score = int(score)  # Преобразуем в целое число
            test = get_object_or_404(Tests, id=test_id)

            # Используем метод update_or_create для создания или обновления записи в модели Points
            point, created = Points.objects.update_or_create(
                user=student,
                test=test,
                defaults={'score': score}
            )

            # Сообщение об успешном добавлении или обновлении
            messages.success(request, f"Оценка успешно {'добавлена' if created else 'обновлена'} для {student.username} - {test.name}.")
        else:
            # Если введена некорректная оценка
            messages.error(request, "Некорректная оценка. Введите положительное целое число.")
    else:
        # Если не все поля заполнены
        messages.error(request, "Все поля должны быть заполнены.")

    # Перенаправляем обратно на страницу с ответами студентов
    return redirect('quiz:all_student_responses')





@login_required
def student_response_detail(request, response_id):
    # Получаем ответ студента по ID
    response = get_object_or_404(TestResponse2, id=response_id)

    # Получаем информацию о тесте и вопросах с ответами
    test = response.test
    multy_test = response.multy_test
    selected_answers = response.selected_answers.all()  # Множественные выбранные ответы
    response_text = response.response_text  # Текстовый ответ

    # Преобразуем ответы в более удобный формат для отображения, если нужно
    selected_answers_list = [answer.name for answer in selected_answers]

    return render(request, 'test/student_response_detail.html', {
        'response': response,
        'test': test,
        'multy_test': multy_test,
        'selected_answers': selected_answers_list,  # Передаем список названий выбранных ответов
        'response_text': response_text  # Текстовый ответ
    })


