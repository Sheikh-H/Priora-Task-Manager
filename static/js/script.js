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
const errorFormMessage = document.getElementById(".form-error");

loginForms.forEach((form) => {
  form.addEventListener("submit", function (e) {
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
});

registerForms.forEach((form) => {
  form.addEventListener("submit", function (e) {
    const fname = document.getElementById("fname").value.trim();
    const sname = document.getElementById("sname").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();
    const confPassword = document
      .getElementById("confirm-password")
      .value.trim();

    errorFormMessage.textContent = "";

    if (!fname) {
      e.preventDefault();
      errorFormMessage.textContent = "Please enter your first name!";
      return;
    }

    if (!sname) {
      e.preventDefault();
      errorFormMessage.textContent = "Please enter your last name!";
      return;
    }

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

    if (!confPassword) {
      e.preventDefault();
      errorFormMessage.textContent = "Please confirm your password!";
      return;
    }

    if (password.value !== confPassword.value) {
      e.preventDefault();
      error.textContent = "Passwords do not match.";
    }
  });
});
