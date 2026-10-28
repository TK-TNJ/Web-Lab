
const images = document.querySelectorAll(".gallery img");
const viewer = document.getElementById("viewer");
const slide = document.getElementById("slide");
let index = 0, timer;

function show(i) {
  index = i;
  slide.src = images[index].src;
  viewer.style.display = "block";
  document.querySelector(".gallery").style.display = "none";
}

function change(step) {
  index = (index + step + images.length) % images.length;
  slide.src = images[index].src;
}

function toggle() {
  if (timer) { clearInterval(timer); timer = null; }
  else timer = setInterval(() => change(1), 2000);
}

function closeView() {
  clearInterval(timer);
  timer = null;
  viewer.style.display = "none";
  document.querySelector(".gallery").style.display = "grid";
}
