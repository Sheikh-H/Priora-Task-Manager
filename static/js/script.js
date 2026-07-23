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

const errorFormMessage = document.querySelector(".form-error");
const loginForm = document.querySelector("#login-form");
if (loginForm) {
  loginForm.addEventListener("submit", function (e) {
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();

    if (password.length < 10) {
      e.preventDefault();
      errorFormMessage.textContent =
        "Password must be greater than 10 characters";
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
  });
}
const registerForm = document.querySelector("#register-form");

if (registerForm) {
  registerForm.addEventListener("submit", function (e) {
    const fname = document.getElementById("fname").value.trim();
    const sname = document.getElementById("sname").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();
    const confPassword = document
      .getElementById("confirm-password")
      .value.trim();

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

    if (password.length < 10) {
      e.preventDefault();
      errorFormMessage.textContent =
        "Password must be greater than 10 characters";
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

    if (password !== confPassword) {
      e.preventDefault();
      error.textContent = "Passwords do not match.";
    }
  });
}
