
console.log('noise-arch radio init.');

async function nowPlaying(){
  const response = await fetch("/playing.json");
  return await response.json();
}

function addArtwork(playing){
  const item = playing.metadata.identifier;
  const art = document.getElementById('artwork');
  art.innerHTML = '';
  const candidates = playing.files
    .filter(f => f.source === "original")
    .filter(f => ['jpg', 'jpeg', 'png', 'gif'].includes(f.format.toLowerCase()));
  const hashes = [];
  const images = [];
  candidates.forEach(img => { 
    if(!hashes.includes(img.sha1)){
      images.push(img.name);
    }
    hashes.push(img.sha1);
  });
  images.forEach(name => {
    const col = document.createElement('div');
    col.classList.add('col');
    const img = document.createElement('img');
    img.classList.add('img-fluid')
    img.classList.add('coverimg')
    img.src = `/items/${item}/${name}`;
    col.appendChild(img);
    art.appendChild(col);
  });
}

// Returns time in seconds since the start time in playing.json
function timeIntoFile(playing){
  const epochSec = Date.now()/1000.0;
  const delta = epochSec - playing.start;
  return delta;
}

function percentIntoFile(playing){
  const epochSec = Date.now()/1000.0;
  const delta = epochSec - playing.start;
  const playingFile = playing.files.find(file => file.name == playing.file);
  return 100.0 * delta / playingFile.length;
}

function pad2(x){
  const result = `${x}`;
  if(result.length < 2){
    return '0' + result;
  }
  return result;
}

// TODO: Consider if just min:sec is enough (forgetting hours)
function hms(t){
  const h = Math.floor(t/(60*60));
  const m = Math.floor((t - h*60*60) / (60));
  const s = Math.floor((t-(h*60*60)-(m*60)));
  return `${pad2(h)}:${pad2(m)}:${pad2(s)}`;
}

var playing;
var progressTimer;

function updateProgress(playing){
  const progressTime = timeIntoFile(playing);
  // TODO: If it's negative we need to re-fetch because a new file is probably playing
  // TODO: If it's too low, we probably need to start our frequent polly poller
  document.getElementById('progressbar-value').innerText = hms(progressTime);
  document.getElementById('progressbar-value').style.width = `${percentIntoFile(playing)}%`;
}

function setupProgress(playing){
  const playingFile = playing.files.find(file => file.name == playing.file);
  console.log(`progress for ${playingFile}`);
  const prog = document.getElementById('progressbar');
  prog.setAttribute('aria-valuemax', parseFloat(playingFile.length));
  console.log(`file is ${hms(playingFile.length)}`)
  console.log(`percent = ${percentIntoFile(playing)}`)
  document.getElementById('duration').innerText = hms(playingFile.length);
  updateProgress(playing);
  setInterval(() => {
    updateProgress(playing);
  }, 333);
}

function startPlayback(){
  console.log("starting playback");
  const player = document.getElementById("audioplayer");
  player.src = `/noise-arch?cachebust=${Date.now()}`
  player.play();
  document.getElementById('playbutton').style.display = 'none';
  document.getElementById('stopbutton').style.display = 'inline-block';
}

function stopPlayback(){
  const player = document.getElementById("audioplayer");
  player.pause();
  player.currentTime = 0;
  document.getElementById('playbutton').style.display = 'inline-block';
  document.getElementById('stopbutton').style.display = 'none';
}

nowPlaying().then(playing => { 
  console.log(playing);
  const item = playing.metadata.identifier;
  const title = playing.metadata.title;
  const a = document.createElement('a');
  a.title = title;
  a.innerText = title.replace(/^NOISE-ARCH: /, '');
  a.target = '_blank';
  a.href = `https://archive.org/details/${item}`;
  document.getElementById('playing-title').appendChild(a);
  addArtwork(playing);
  setupProgress(playing);
});