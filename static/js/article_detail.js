const thumbs = document.querySelector(".thumb-img").children;
const changeImage = (event) => {
  document.querySelector(".pro-img").src = event.children[0].src;
  for (let i = 0; i < thumbs.length; i++) {
    thumbs[i].classList.remove("active");
  }
  event.classList.add("active");
};

thumbs[0].classList.add("active");
