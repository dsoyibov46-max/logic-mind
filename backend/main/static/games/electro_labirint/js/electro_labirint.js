const grid = document.getElementById("grid");
const levelSpan = document.getElementById("level");
const movesSpan = document.getElementById("moves");
const starsSpan = document.getElementById("stars");
const message = document.getElementById("message");

let level = 1;
let size = 4;
let bulbCount = 2;
let moves = 0;
let maxMoves = 20;
let tiles = [];
let history = [];
let timer = 0;
let timerInterval;

// INIT
function init(){
    grid.innerHTML = "";
    tiles = [];
    history = [];
    moves = 0;
    movesSpan.textContent = moves;
    message.textContent = "";

    if(level%3===0) bulbCount = Math.min(4, bulbCount+1);
    if(level%4===0) size = Math.min(7, size+1);
    
    maxMoves = Math.floor(size*3 + bulbCount);
    document.getElementById("maxMoves").textContent = maxMoves;
    
    grid.style.gridTemplateColumns = `repeat(${size},70px)`;

    clearInterval(timerInterval);
    timer = 0;
    timerInterval = setInterval(()=>{
        timer++;
        document.getElementById("timer").textContent = timer;
    },1000);

    // Lampalarni random joylash
    let bulbPositions = [];
    while(bulbPositions.length < bulbCount){
        let r = Math.floor(Math.random()*(size*size-1))+1;
        if(!bulbPositions.includes(r)) bulbPositions.push(r);
    }

    // Tiles yaratish
    for(let i=0;i<size*size;i++){
        let tile = document.createElement("div");
        tile.classList.add("tile");
        tile.dataset.rotation = 0;
        tile.dataset.type = "wire";
        tile.dataset.connections = "1010";

        if(i===0){
            tile.textContent = "🔋";
            tile.classList.add("power");
            tile.dataset.type="power";
            tile.dataset.connections="1111";
        } else if(bulbPositions.includes(i)){
            tile.textContent = "💡";
            tile.classList.add("bulb");
            tile.dataset.type="bulb";
            tile.dataset.connections="1111";
        } else {
            randomizeWire(tile);
        }

        tile.addEventListener("click",()=>rotate(tile));
        grid.appendChild(tile);
        tiles.push(tile);
    }

    checkPower();
}

// Random wire generator — qiyinlashtirilgan
function randomizeWire(tile){
    const types = [
        "1100","0110","0011","1001", // corner 50%
        "1110","0111","1011","1101", // T 40%
        "1010","0101"                 // straight 10%
    ];
    tile.dataset.connections = types[Math.floor(Math.random()*types.length)];
    drawWire(tile);
}

// Draw wire with charge particles
function drawWire(tile){
    const conn = tile.dataset.connections;
    tile.innerHTML="";
    const center = document.createElement("div");
    center.classList.add("center-point");
    tile.appendChild(center);
    const directions=["up","right","down","left"];
    for(let i=0;i<4;i++){
        if(conn[i]==="1"){
            const part=document.createElement("div");
            part.classList.add("wire-part",directions[i]);
            for(let j=0;j<3;j++){
                const particle=document.createElement("div");
                particle.classList.add("charge-particle");
                particle.style.setProperty("--particle-index",j);
                part.appendChild(particle);
            }
            tile.appendChild(part);
        }
    }
    if(tile.dataset.type==="power") tile.innerHTML+='<div style="position:absolute;z-index:5">🔋</div>';
    if(tile.dataset.type==="bulb") tile.innerHTML+='<div style="position:absolute;z-index:5">💡</div>';
}

// Rotate tile
function rotate(tile){
    if(tile.dataset.type!=="wire") return;
    if(moves>=maxMoves){lose();return;}
    history.push({tile:tile,rotation:tile.dataset.rotation,connections:tile.dataset.connections});
    let currentRot = parseInt(tile.dataset.rotation)+90;
    tile.dataset.rotation = currentRot;
    tile.style.transform = `rotate(${currentRot}deg)`;
    let c=tile.dataset.connections; c=c.slice(3)+c.slice(0,3);
    tile.dataset.connections=c;
    moves++;
    movesSpan.textContent = moves;
    setTimeout(checkPower,150);
}

// Undo, Shuffle, Hint
function undo(){let last=history.pop();if(!last) return; last.tile.dataset.rotation=last.rotation;last.tile.dataset.connections=last.connections;last.tile.style.transform=`rotate(${last.rotation}deg)`;drawWire(last.tile);moves--;movesSpan.textContent=moves;checkPower();}
function shuffle(){tiles.forEach(tile=>{if(tile.dataset.type==="wire"){let r=Math.floor(Math.random()*4);tile.dataset.rotation=r*90;tile.style.transform=`rotate(${r*90}deg)`;drawWire(tile);}});checkPower();}
function hint(){tiles.forEach(tile=>{if(tile.dataset.type==="wire"){tile.style.boxShadow="0 0 10px cyan";setTimeout(()=>{tile.style.boxShadow="";},700);}});}

// Helper
function indexToRC(i){return[Math.floor(i/size),i%size];}
function rcToIndex(r,c){return r*size+c;}

// Check power connections
function checkPower(){
    tiles.forEach(t=>t.classList.remove("active"));
    let visited=new Set();
    let queue=[0]; visited.add(0);
    while(queue.length){
        let i=queue.shift();
        tiles[i].classList.add("active");
        let [r,c]=indexToRC(i);
        let conn=tiles[i].dataset.connections;
        let directions=[[-1,0,0,2],[0,1,1,3],[1,0,2,0],[0,-1,3,1]];
        directions.forEach(([dr,dc,side,opp])=>{
            let nr=r+dr,nc=c+dc; if(nr<0||nc<0||nr>=size||nc>=size) return;
            let ni=rcToIndex(nr,nc); if(visited.has(ni)) return;
            let nConn = tiles[ni].dataset.connections;
            if(conn[side]==="1" && nConn[opp]==="1"){visited.add(ni);queue.push(ni);}
        });
    }

    let allBulbsOn=true;
    tiles.forEach((tile,i)=>{
        if(tile.dataset.type==="bulb"){
            if(visited.has(i)) tile.classList.add("on");
            else {tile.classList.remove("on"); allBulbsOn=false;}
        }
    });

    if(allBulbsOn) win();
}

// WIN / NEXT LEVEL / RESTART
function win(){
    clearInterval(timerInterval);
    giveStars();
    const winScreen=document.getElementById("winScreen");
    const winStars=document.getElementById("winStars");
    winStars.textContent = starsSpan.textContent;
    winScreen.style.display="flex";
    confetti({particleCount:200,spread:120});
    saveProgress();
    sendResult(100, timer, level);
    function sendResult(score, time, level) {
    fetch("/results/save/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            game_id: 1,
            score: score,
            time_spent: time,
            level_reached: level
        })
    })
    .then(res => res.json())
    .then(data => {
        console.log("Natija saqlandi:", data);
    });
}
}

function nextLevel(){document.getElementById("winScreen").style.display="none"; level++; levelSpan.textContent=level; init();}
function restartGame(){document.getElementById("winScreen").style.display="none"; init();}

// Stars
function giveStars(){
    if(moves<=size*2) starsSpan.textContent="⭐⭐⭐";
    else if(moves<=size*3) starsSpan.textContent="⭐⭐";
    else starsSpan.textContent="⭐";
}

// Save / Load
function saveProgress(){localStorage.setItem("electroLevel",level);}
function loadProgress(){let saved=localStorage.getItem("electroLevel"); if(saved){level=parseInt(saved); levelSpan.textContent=level;}}
loadProgress();
init();

function sendResult(score, time, level) {
    fetch("/results/save/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            game_id: 1,
            score: score,
            time_spent: time,
            level_reached: level
        })
    })
    .then(async res => {
        const text = await res.text();
        console.log("SERVER RESPONSE:", text);
        try {
            return JSON.parse(text);
        } catch (e) {
            throw new Error("Server JSON qaytarmadi");
        }
    })
    .then(data => console.log("Natija:", data))
    .catch(err => console.error("XATO:", err));
}
