document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById('warningModal');
    const closeModal = document.getElementById('closeModal');
    const startTestButton = document.getElementById('startTest');
    const cancelTestButton = document.getElementById('cancelTest');

    // Показать модальное окно
    document.querySelectorAll('.start-quiz').forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            const quizId = this.getAttribute('data-quiz-id');
            // Сохранить идентификатор теста для дальнейшего использования
            localStorage.setItem('currentQuizId', quizId);
            modal.style.display = 'flex';
        });
    });

    // Закрытие модального окна
    closeModal.addEventListener('click', function () {
        modal.style.display = 'none';
    });

    // Начать тест
    startTestButton.addEventListener('click', function () {
        const quizId = localStorage.getItem('currentQuizId');
        if (quizId) {
            // Замените URL на фактический маршрут вашего теста
            window.location.href = `/quiz/${quizId}/`;
        }
    });

    // Отмена
    cancelTestButton.addEventListener('click', function () {
        modal.style.display = 'none';
    });
});
