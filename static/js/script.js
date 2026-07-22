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

const elements = document.querySelectorAll(
  ".hidden-right, .hidden-left, .hidden-up",
);

elements.forEach((element) => observer.observe(element));

featureCards = document.querySelectorAll(".feature-info");

featureCards.forEach((card, index) => {
  card.style.transitionDelay = `${index * 500}ms`;
});

featureAnimations = document.querySelectorAll(".feature-animation");

featureAnimations.forEach((card, index) => {
  card.style.transitionDelay = `${index * 500}ms`;
});

nightModeButton = document.querySelector(".night-mode-button");
nightModeInnerButton = document.querySelector(".night-mode-inner-button");

nightModeButton.addEventListener("click", () => {
  nightModeInnerButton.classList.toggle("active");
  nightModeButton.classList.toggle("active");
  document.documentElement.classList.toggle("dark-mode");
});

setTimeout(() => {
  const flashes = document.querySelectorAll(".flash");
  flashes.forEach((flash) => {
    flash.remove();
  });
}, 3000);

const loginForms = document.querySelectorAll("#login-form");
const registerForms = document.querySelectorAll("#register-form");
const errorFormMessage = document.querySelectorAll(".form-error");

loginForms.addEventListener("submit", function (e) {
  const email = document.getElementById("email");
  const password = document.getElementById("password");

  if (!email) {
    e.preventDefault();
    errorFormMessage.textContent = "Please enter your email!";
    return;
  }
  if (!password) {
    e.preventDefault();
    errorFormMessage.textContent = "Please enter your password!";
    return;
  }
});
