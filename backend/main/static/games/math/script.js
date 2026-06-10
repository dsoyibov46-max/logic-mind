/**
 * Logic Mind — Tez Hisoblash O'yini
 * 60 soniya ichida imkon qadar ko'p to'g'ri javob
 * Amallar: +, -, × random
 */

// ─── Amallar
const OPERATIONS = [
    {
        symbol: '+',
        generate: () => {
            const a = Math.floor(Math.random() * 20) + 1;
            const b = Math.floor(Math.random() * 20) + 1;
            return { a, b, answer: a + b };
        }
    },
    {
        symbol: '-',
        generate: () => {
            const a = Math.floor(Math.random() * 20) + 5;
            const b = Math.floor(Math.random() * (a - 1)) + 1;
            return { a, b, answer: a - b };
        }
    },
    {
        symbol: '×',
        generate: () => {
            const a = Math.floor(Math.random() * 9) + 2;
            const b = Math.floor(Math.random() * 9) + 2;
            return { a, b, answer: a * b };
        }
    }
];

// ─── Game state
let currentAnswer = 0;
let score = 0;
let totalQuestions = 0;
let timeLeft = 60;
let timerInterval = null;
let gameActive = false;
let gameStartTime = null;

// ─── DOM Elementlari
const questionEl   = document.getElementById('question');
const optionsEl    = document.getElementById('options');
const resultEl     = document.getElementById('result');
const scoreEl      = document.getElementById('score');
const timerEl      = document.getElementById('timer');
const startBtn     = document.getElementById('startBtn');
const gameOverEl   = document.getElementById('gameOver');
const finalScoreEl = document.getElementById('finalScore');
const finalTotalEl = document.getElementById('finalTotal');
const playAgainBtn = document.getElementById('playAgainBtn');

// ─── Event listeners
startBtn.addEventListener('click', startGame);
playAgainBtn.addEventListener('click', resetGame);

// ─── O'yinni boshlash
function startGame() {
    score = 0;
    totalQuestions = 0;
    timeLeft = 60;
    gameActive = true;
    gameStartTime = Date.now();

    scoreEl.innerText = score;
    timerEl.innerText = timeLeft;
    timerEl.style.color = ''; // Rangni tiklash
    resultEl.innerText = '';
    resultEl.className = '';

    startBtn.style.display = 'none';
    gameOverEl.style.display = 'none';
    optionsEl.style.display = 'grid'; // CSS Grid dizayni uchun 'grid' qilindi
    questionEl.style.display = 'block';

    generateQuestion();

    timerInterval = setInterval(() => {
        timeLeft--;
        timerEl.innerText = timeLeft;

        // Vaqt kam qolganda neon qizil ogohlantirish effekti
        if (timeLeft <= 10) {
            timerEl.style.color = '#ff0055';
            timerEl.style.textShadow = '0 0 15px #ff0055';
        }

        if (timeLeft <= 0) {
            endGame();
        }
    }, 1000);
}

// ─── Savol generatsiya
function generateQuestion() {
    if (!gameActive) return;

    // Random amal tanlash
    const op = OPERATIONS[Math.floor(Math.random() * OPERATIONS.length)];
    const { a, b, answer } = op.generate();
    currentAnswer = answer;

    questionEl.innerText = `${a} ${op.symbol} ${b} = ?`;

    // Javob variantlari — noto'g'rilar mantiqiy bo'lsin
    const wrongAnswers = generateWrongAnswers(answer, op.symbol);
    const options = [answer, ...wrongAnswers].sort(() => Math.random() - 0.5);

    optionsEl.innerHTML = '';
    options.forEach(opt => {
        const btn = document.createElement('button');
        btn.className = 'option-btn';
        btn.innerText = opt;
        btn.addEventListener('click', () => checkAnswer(opt, btn));
        optionsEl.appendChild(btn);
    });
}

// ─── Noto'g'ri javoblar
function generateWrongAnswers(correct, symbol) {
    const wrongs = new Set();
    const attempts = [1, 2, 3, -1, -2, -3, 5, -5, 10, -10];

    for (const diff of attempts.sort(() => Math.random() - 0.5)) {
        const candidate = correct + diff;
        if (candidate !== correct && candidate > 0) {
            wrongs.add(candidate);
        }
        if (wrongs.size === 3) break;
    }

    // Fallback
    while (wrongs.size < 3) {
        const rand = correct + Math.floor(Math.random() * 10) + 1;
        if (rand !== correct) wrongs.add(rand);
    }

    return [...wrongs].slice(0, 3);
}

// ─── Javobni tekshirish
function checkAnswer(value, btn) {
    if (!gameActive) return;

    totalQuestions++;

    // Barcha tugmalarni disable qilish
    optionsEl.querySelectorAll('.option-btn').forEach(b => b.disabled = true);

    if (value === currentAnswer) {
        score++;
        scoreEl.innerText = score;
        btn.classList.add('correct');
        resultEl.innerText = '✅ To\'g\'ri!';
        resultEl.className = 'correct-msg'; // Yangi neon CSS klassi
    } else {
        btn.classList.add('wrong');
        resultEl.innerText = `❌ Noto\'g\'ri!`;
        resultEl.className = 'wrong-msg'; // Yangi neon CSS klassi

        // To'g'ri javobni ham neon yashil qilib ko'rsatish
        optionsEl.querySelectorAll('.option-btn').forEach(b => {
            if (parseInt(b.innerText) === currentAnswer) {
                b.classList.add('correct');
            }
        });
    }

    setTimeout(() => {
        resultEl.innerText = '';
        resultEl.className = '';
        generateQuestion();
    }, 800);
}

// ─── O'yin tugashi
function endGame() {
    clearInterval(timerInterval);
    gameActive = false;

    const timeSpent = Math.round((Date.now() - gameStartTime) / 1000);

    optionsEl.style.display = 'none';
    questionEl.style.style = 'none'; // yashirish uchun inline style o'rniga display ishlatiladi
    questionEl.style.display = 'none';
    resultEl.innerText = '';
    resultEl.className = '';

    finalScoreEl.innerText = score;
    finalTotalEl.innerText = totalQuestions;
    gameOverEl.style.display = 'block';

    saveGameResult(score, timeSpent);
}

// ─── Qayta o'ynash
function resetGame() {
    timerEl.style.color = '';
    timerEl.style.textShadow = '';
    startBtn.style.display = 'block';
    gameOverEl.style.display = 'none';
    optionsEl.style.display = 'none';
    questionEl.style.display = 'none';
    questionEl.innerText = '';
    scoreEl.innerText = '0';
    timerEl.innerText = '60';
    resultEl.innerText = '';
    resultEl.className = '';
}

// ─── CSRF token olish
function getCsrfToken() {
    const name = 'csrftoken';
    for (const cookie of document.cookie.split(';')) {
        const c = cookie.trim();
        if (c.startsWith(name + '=')) {
            return decodeURIComponent(c.substring(name.length + 1));
        }
    }
    return '';
}

// ─── Natijani backendga saqlash
function saveGameResult(score, timeSpent) {
    if (typeof GAME_ID === 'undefined' || isNaN(GAME_ID)) {
        console.error('❌ GAME_ID aniqlanmagan. HTML templateda const GAME_ID = parseInt("{{ game.id }}"); qo\'shing.');
        return;
    }

    fetch('/results/save/', {
        method: 'POST',
        headers: {
            // Sarlavhalar va ma'lumot uzatish
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        },
        credentials: 'same-origin',
        body: JSON.stringify({
            game_id: GAME_ID,
            score: score,
            time_spent: timeSpent,
            level_reached: 1
        })
    })
    .then(res => {
        if (!res.ok) return res.json().then(err => Promise.reject(err));
        return res.json();
    })
    .then(data => {
        if (data.status === 'success') {
            console.log('✅ Natija saqlandi. ID:', data.result_id);
        } else {
            console.warn('⚠️ Backend xato:', data.message);
        }
    })
    .catch(err => {
        console.error('❌ Saqlashda xato:', err);
    });
}