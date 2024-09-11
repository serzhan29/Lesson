document.addEventListener("DOMContentLoaded", function () {
    const timerElement = document.getElementById('quiz-timer');
    if (!timerElement) {
        console.error("Элемент с ID 'quiz-timer' не найден.");
        return;
    }

    const quizForm = document.getElementById('quizForm');
    let timeLeft = localStorage.getItem('timeLeft') ? parseInt(localStorage.getItem('timeLeft'), 10) : 30 * 60; // 30 минут в секундах

    function updateTimer() {
        const minutes = Math.floor(timeLeft / 60);
        const seconds = timeLeft % 60;
        timerElement.textContent = `Осталось: ${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;

        if (timeLeft <= 0) {
            clearInterval(timerInterval);
            alert("Уақыт өтті! Тест автоматты түрде жіберіледі.");
            quizForm.submit(); // Автоматическая отправка формы по истечению времени
        }

        timeLeft--; // Уменьшаем время на 1 секунду
        localStorage.setItem('timeLeft', timeLeft); // Сохраняем оставшееся время
    }

    const timerInterval = setInterval(updateTimer, 1000); // Обновление каждую секунду
    updateTimer(); // Запуск функции для первоначального обновления

    // Обработка закрытия окна или перехода на другую страницу
    window.addEventListener('beforeunload', function () {
        localStorage.setItem('timeLeft', timeLeft);
    });
});
