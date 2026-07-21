const observer = new IntersectionObserver(
  (entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("show");
        observer.unobserve(entry.target);
      }
    });
  },
  {
    treshold: 0.2,
  },
);

const elements = document.querySelectorAll(".hidden-right, .hidden-left");

elements.forEach((element) => observer.observe(element));

featureCards = document.querySelectorAll(".feature-info");

featureCards.forEach((card, index) => {
  card.style.transitionDelay = `${index * 500}ms`;
});

featureAnimations = document.querySelectorAll(".feature-animation");

featureAnimations.forEach((card, index) => {
  card.style.transitionDelay = `${index * 500}ms`;
});

nightModeButton = document.querySelector(".night-mode-inner-button");

nightModeButton.addEventListener("click", () => {
  nightModeButton.classList.toggle("active");
});
