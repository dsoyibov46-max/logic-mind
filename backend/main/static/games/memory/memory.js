/**
 * Logic Mind — Memory Game
 * Fixed: result saving, CSRF auth, correct field names, duplicate function removed
 */

// ─── GAME_ID: Django template dan keladi (memory_game.html ichida)
// <script> const GAME_ID = {{ game.id }}; </script>

// ─── Levels konfiguratsiyasi
const LEVELS = {
    1: ["rocket.png", "camera.png", "headphone.png", "gamepad.png"],
    2: ["rocket.png", "camera.png", "headphone.png", "gamepad.png", "coffee.png", "bike.png"],
    3: ["rocket.png", "camera.png", "headphone.png", "gamepad.png", "coffee.png", "bike.png", "vr.png", "drone.png"]
};

const MAX_LEVEL = Object.keys(LEVELS).length;
const TIME_PER_LEVEL = 60;

// ─── Game state
let timeLeft = TIME_PER_LEVEL;
let timerInterval = null;
let currentLevel = 1;
let score = 0;
let moves = 0;
let openedCards = [];
let matchedPairs = 0;
let isLocked = false;   // karta flip pauzasi uchun
let gameStartTime = null;

// ─── DOM elementlari
const grid        = document.getElementById("grid");
const scoreEl     = document.getElementById("score");
const movesEl     = document.getElementById("moves");
const levelEl     = document.getElementById("level");
const timerEl     = document.getElementById("timer");
const winModal    = document.getElementById("winModal");
const finalScore  = document.getElementById("finalScore");
const restartBtn  = document.getElementById("restartBtn");

// ─── Restart tugmasi
restartBtn.addEventListener("click", () => {
    currentLevel = 1;
    score = 0;
    scoreEl.innerText = score;
    startLevel();
});

// ─── CSRF token — Django session auth uchun
function getCsrfToken() {
    const name = "csrftoken";
    for (const cookie of document.cookie.split(";")) {
        const c = cookie.trim();
        if (c.startsWith(name + "=")) {
            return decodeURIComponent(c.substring(name.length + 1));
        }
    }
    return "";
}

// ─── Level boshlash
function startLevel() {
    clearInterval(timerInterval);

    timeLeft = TIME_PER_LEVEL;
    timerEl.innerText = timeLeft;
    gameStartTime = Date.now();

    // modal yashirish
    winModal.style.display = "none";

    // state reset
    openedCards = [];
    matchedPairs = 0;
    moves = 0;
    isLocked = false;

    movesEl.innerText = moves;
    levelEl.innerText = currentLevel;

    // kartalar
    buildGrid();

    // timer
    timerInterval = setInterval(() => {
        timeLeft--;
        timerEl.innerText = timeLeft;

        if (timeLeft <= 0) {
            clearInterval(timerInterval);
            handleTimeOut();
        }
    }, 1000);
}

// ─── Grid qurilish
function buildGrid() {
    grid.innerHTML = "";

    const images = LEVELS[currentLevel];
    const pairs = [...images, ...images];
    const shuffled = pairs.sort(() => Math.random() - 0.5);

    grid.style.gridTemplateColumns = "repeat(4, 120px)";

    shuffled.forEach((img) => {
        const card = document.createElement("div");
        card.className = "card";
        card.dataset.emoji = img;
        card.innerHTML = `<div class="card-back">🧠</div>`;
        card.addEventListener("click", () => flipCard(card));
        grid.appendChild(card);
    });
}

// ─── Karta ochish
function flipCard(card) {
    if (
        isLocked ||
        openedCards.length >= 2 ||
        card.classList.contains("flipped") ||
        card.classList.contains("matched")
    ) return;

    card.classList.add("flipped");
    card.innerHTML = `<img src="${IMAGE_BASE}${card.dataset.emoji}" class="card-image" alt="${card.dataset.emoji}">`;

    openedCards.push(card);

    if (openedCards.length === 2) {
        moves++;
        movesEl.innerText = moves;
        checkMatch();
    }
}

// ─── Juftlik tekshirish
function checkMatch() {
    const [first, second] = openedCards;

    if (first.dataset.emoji === second.dataset.emoji) {
        first.classList.add("matched");
        second.classList.add("matched");

        matchedPairs++;
        score += 10;
        scoreEl.innerText = score;
        openedCards = [];

        checkLevelComplete();
    } else {
        isLocked = true;
        setTimeout(() => {
            first.classList.remove("flipped");
            second.classList.remove("flipped");
            first.innerHTML = `<div class="card-back">🧠</div>`;
            second.innerHTML = `<div class="card-back">🧠</div>`;
            openedCards = [];
            isLocked = false;
        }, 700);
    }
}

// ─── Level tugash tekshiruvi
function checkLevelComplete() {
    const totalPairs = LEVELS[currentLevel].length;

    if (matchedPairs === totalPairs) {
        clearInterval(timerInterval);

        const timeSpent = Math.round((Date.now() - gameStartTime) / 1000);

        saveGameResult(score, timeSpent, currentLevel);

        // win modal
        finalScore.innerText = `Score: ${score} | Level: ${currentLevel} | Moves: ${moves}`;
        winModal.style.display = "flex";
    }
}

// ─── Keyingi level (modal tugmasi)
function nextLevel() {
    if (currentLevel < MAX_LEVEL) {
        currentLevel++;
        startLevel();
    } else {
        winModal.style.display = "none";
        alert("🏆 Tabriklaymiz! Siz barcha levelni tugatdingiz!");
    }
}

// ─── Vaqt tugashi
function handleTimeOut() {
    isLocked = true;
    alert("⏰ Vaqt tugadi! Qaytadan urinib ko'ring.");
    startLevel();
}

// ─── Natijani backendga saqlash
function saveGameResult(score, timeSpent, levelReached) {

    // GAME_ID HTML templateda aniqlanishi kerak:
    // <script>const GAME_ID = {{ game.id }};</script>
    if (typeof GAME_ID === "undefined") {
        console.error("❌ GAME_ID aniqlanmagan. HTML templateda const GAME_ID = {{ game.id }}; qo'shing.");
        return;
    }

    const payload = {
        game_id: GAME_ID,
        score: score,
        time_spent: timeSpent,
        level_reached: levelReached
    };

    fetch("/results/save/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCsrfToken()
        },
        credentials: "same-origin",
        body: JSON.stringify(payload)
    })
    .then(res => {
        if (!res.ok) {
            return res.json().then(err => Promise.reject(err));
        }
        return res.json();
    })
    .then(data => {
        if (data.status === "success") {
            console.log("✅ Natija saqlandi. ID:", data.result_id);
        } else {
            console.warn("⚠️ Backend xato:", data.message);
        }
    })
    .catch(err => {
        console.error("❌ Saqlashda xato:", err);
    });
}

// ─── O'yinni boshlash
startLevel();