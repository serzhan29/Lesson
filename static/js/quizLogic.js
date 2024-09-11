document.addEventListener("DOMContentLoaded", function () {
    let currentQuestion = 0;
    const questions = document.querySelectorAll('.quiz-question');
    const nextButton = document.getElementById('nextQuestion');
    const prevButton = document.getElementById('prevQuestion');
    const submitButton = document.getElementById('submitQuiz');
    const quizForm = document.getElementById('quizForm');

    // Load saved answers from local storage
    function loadSavedAnswers() {
        const savedAnswers = JSON.parse(localStorage.getItem('quizAnswers')) || {};
        questions.forEach((question) => {
            const questionId = question.id.split('_')[1]; // Extract question ID
            const savedAnswer = savedAnswers[questionId];
            if (savedAnswer) {
                savedAnswer.forEach(answerId => {
                    const input = document.getElementById(`answer_${answerId}`);
                    if (input) {
                        input.checked = true;
                    }
                });
            }
        });
    }

    // Save selected answers to local storage
    function saveSelectedAnswers() {
        const answers = {};
        questions.forEach((question) => {
            const questionId = question.id.split('_')[1]; // Extract question ID
            const checkedInputs = Array.from(question.querySelectorAll('input:checked'));
            answers[questionId] = checkedInputs.map(input => input.value);
        });
        localStorage.setItem('quizAnswers', JSON.stringify(answers));
    }

    function showQuestion(index) {
        questions.forEach((q, i) => {
            q.style.display = i === index ? 'block' : 'none';
        });
        prevButton.disabled = index === 0;
        nextButton.style.display = index === questions.length - 1 ? 'none' : 'inline-block';
        submitButton.style.display = index === questions.length - 1 ? 'inline-block' : 'none';
    }

    // Обработка кликов на кнопки
    nextButton.addEventListener('click', function () {
        if (currentQuestion < questions.length - 1) {
            saveSelectedAnswers(); // Save answers before navigating
            currentQuestion++;
            showQuestion(currentQuestion);
        }
    });

    prevButton.addEventListener('click', function () {
        if (currentQuestion > 0) {
            saveSelectedAnswers(); // Save answers before navigating
            currentQuestion--;
            showQuestion(currentQuestion);
        }
    });

    // Инициализация с первого вопроса и загрузка сохраненных ответов
    showQuestion(currentQuestion);
    loadSavedAnswers(); // Load answers on page load

    // Clear saved answers on form submit
    quizForm.addEventListener('submit', function () {
        localStorage.removeItem('quizAnswers');
    });
});
