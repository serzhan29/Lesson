from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Assignment, StudentSubmission, Question, StudentAnswer
from django.contrib.auth.decorators import login_required


@login_required
def assignment_list(request):
    """Список всех заданий"""
    assignments = Assignment.objects.all()

    # Фильтруем только те submissions, у которых задания существуют
    submissions = StudentSubmission.objects.filter(
        student=request.user,
        assignment__isnull=False
    )

    # Получаем ID заданий, которые студент уже сдал
    submitted_assignments = submissions.values_list('assignment_id', flat=True)

    return render(request, 'task/task_list.html', {
        'assignments': assignments,
        'submitted_assignments': submitted_assignments
    })



@login_required
def assignment_view(request, assignment_id):
    """Просмотр задания и отправка ответов"""
    assignment = get_object_or_404(Assignment, id=assignment_id)
    questions = assignment.questions.all()

    # Проверка, существует ли уже отправка для этого задания
    existing_submission = StudentSubmission.objects.filter(
        assignment=assignment,
        student=request.user
    ).first()

    if request.method == "POST":
        if existing_submission:
            messages.warning(request, 'Вы уже отправили ответы на это задание.')
            return redirect('assignment_list')

        # Создаем объект StudentSubmission
        submission = StudentSubmission.objects.create(
            assignment=assignment,
            student=request.user,
        )

        # Обработка ответов от пользователя
        for question in questions:
            answer_text = request.POST.get(f'answer_{question.id}')
            if answer_text:  # Если ответ не пустой
                # Создаем новый объект StudentAnswer
                StudentAnswer.objects.create(
                    submission=submission,
                    question=question,
                    answer=answer_text,
                )

        messages.success(request, 'Ваши ответы успешно отправлены!')
        return redirect('assignment_list')  # Перенаправляем на список заданий

    return render(request, 'task/task.html', {
        'assignment': assignment,
        'questions': questions,
    })



