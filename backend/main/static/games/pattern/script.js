const patterns = [
  { seq: ["▲", "●", "▲", "●", "?"], answer: "▲", options: ["▲", "■", "★"] },
  { seq: ["■", "■", "●", "■", "■", "?"], answer: "●", options: ["●", "▲", "★"] }
];

let current = null;

function loadPattern() {
  current = patterns[Math.floor(Math.random() * patterns.length)];
  document.getElementById("pattern").innerText = current.seq.join(" ");
  const optionsDiv = document.getElementById("options");
  optionsDiv.innerHTML = "";

  current.options.forEach(opt => {
    const btn = document.createElement("button");
    btn.innerText = opt;
    btn.onclick = () => checkPattern(opt);
    optionsDiv.appendChild(btn);
  });
}

function checkPattern(value) {
  if (value === current.answer) {
    document.getElementById("result").innerText = "To'g'ri!";
    saveGameStat("pattern", 1);
  } else {
    document.getElementById("result").innerText = "Noto'g'ri!";
  }

  setTimeout(loadPattern, 1000);
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
      duration_seconds: 15
    })
  });
}

loadPattern();