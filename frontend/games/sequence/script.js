let currentAnswer = 0;

function generateSequence() {
  const start = Math.floor(Math.random() * 5) + 1;
  const step = Math.floor(Math.random() * 5) + 2;
  const seq = [];

  for (let i = 0; i < 5; i++) {
    seq.push(start + step * i);
  }

  currentAnswer = seq[4];

  document.getElementById("question").innerText =
    `${seq[0]}, ${seq[1]}, ${seq[2]}, ${seq[3]}, ?`;

  const options = [
    currentAnswer,
    currentAnswer + 2,
    currentAnswer - 2,
    currentAnswer + 4
  ].sort(() => Math.random() - 0.5);

  const optionsDiv = document.getElementById("options");
  optionsDiv.innerHTML = "";

  options.forEach(opt => {
    const btn = document.createElement("button");
    btn.innerText = opt;
    btn.onclick = () => checkAnswer(opt);
    optionsDiv.appendChild(btn);
  });
}

function checkAnswer(value) {
  const result = document.getElementById("result");
  if (value === currentAnswer) {
    result.innerText = "To'g'ri!";
    saveGameStat("sequence", 1);
  } else {
    result.innerText = "Noto'g'ri!";
  }
  setTimeout(generateSequence, 1000);
}

function saveGameStat(gameType, score) {
  const token = localStorage.getItem("access_token");
  if (!token) return;

  fetch("http://127.0.0.1:8000/api/stats/save/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    },
    body: JSON.stringify({
      game: gameType,
      score: score,
      duration_seconds: 20
    })
  });
}

generateSequence();