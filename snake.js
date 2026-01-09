(function(){
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const block = 10;
const width = canvas.width;
const height = canvas.height;
let speed = 10; // frames per second
let snake = [{x: Math.floor(width/2/block)*block, y: Math.floor(height/2/block)*block}];
let dir = {x:0, y:0};
let food = {};
let score = 0;
let gameOver = false;
const scoreEl = document.getElementById('score');
const overlay = document.getElementById('overlay');
const restartBtn = document.getElementById('restart');

function spawnFood(){
  food.x = Math.floor(Math.random()*(width/block)) * block;
  food.y = Math.floor(Math.random()*(height/block)) * block;
  for (let s of snake){ if (s.x===food.x && s.y===food.y){ spawnFood(); return; } }
}
function reset(){
  snake = [{x: Math.floor(width/2/block)*block, y: Math.floor(height/2/block)*block}];
  dir = {x:0,y:0};
  score = 0;
  gameOver = false;
  overlay.classList.add('hidden');
  spawnFood();
  updateScore();
}
function updateScore(){ scoreEl.textContent = 'Score: ' + score; }
function draw(){
  ctx.fillStyle = '#3268b8';
  ctx.fillRect(0,0,width,height);
  ctx.fillStyle = '#00ff00';
  ctx.fillRect(food.x, food.y, block, block);
  ctx.fillStyle = '#ffffff';
  for (let s of snake) ctx.fillRect(s.x, s.y, block, block);
}
function step(){
  if (gameOver) return;
  // If the player hasn't started moving yet, don't advance the game
  if (dir.x === 0 && dir.y === 0) { draw(); return; }
  const head = {x: snake[snake.length-1].x + dir.x*block, y: snake[snake.length-1].y + dir.y*block};
  if (head.x < 0 || head.x >= width || head.y < 0 || head.y >= height){ endGame(); return; }
  // Check collision with the snake body (exclude the current tail/head depending on movement)
  for (let i = 0; i < snake.length; i++){
    const seg = snake[i];
    if (seg.x===head.x && seg.y===head.y){ endGame(); return; }
  }
  snake.push(head);
  if (head.x===food.x && head.y===food.y){ score += 1; updateScore(); spawnFood(); }
  else { snake.shift(); }
  draw();
}
function endGame(){
  gameOver = true;
  document.getElementById('msg').textContent = 'Game Over! Score: ' + score;
  overlay.classList.remove('hidden');
}
document.addEventListener('keydown', (e)=>{
  if (e.key==='ArrowLeft' && dir.x===0){ dir = {x:-1,y:0}; }
  else if (e.key==='ArrowRight' && dir.x===0){ dir = {x:1,y:0}; }
  else if (e.key==='ArrowUp' && dir.y===0){ dir = {x:0,y:-1}; }
  else if (e.key==='ArrowDown' && dir.y===0){ dir = {x:0,y:1}; }
});
restartBtn.addEventListener('click', reset);
    // Start button to begin movement without needing a keypress
    const startBtn = document.getElementById('startGame');
    function startGame(){
      if (dir.x === 0 && dir.y === 0){
        dir = {x:1,y:0};
      }
      overlay.classList.add('hidden');
      // focus canvas so arrow keys work immediately
      canvas.focus && canvas.focus();
    }
    if (startBtn) startBtn.addEventListener('click', startGame);
spawnFood();
draw();
setInterval(step, 1000/speed);
})();
