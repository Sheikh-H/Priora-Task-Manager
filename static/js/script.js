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
    threshold: 0.2,
  },
);

const elements = document.querySelectorAll(
  ".hidden-right, .hidden-left, .hidden-up",
);

elements.forEach((element) => observer.observe(element));

const featureCards = document.querySelectorAll(".feature-info");

featureCards.forEach((card, index) => {
  card.style.transitionDelay = `${index * 500}ms`;
});

const featureAnimations = document.querySelectorAll(".feature-animation");

featureAnimations.forEach((card, index) => {
  card.style.transitionDelay = `${index * 500}ms`;
});

const nightModeButton = document.querySelector(".night-mode-button");
const nightModeInnerButton = document.querySelector(".night-mode-inner-button");

if (nightModeButton) {
  nightModeButton.addEventListener("click", () => {
    nightModeInnerButton.classList.toggle("active");
    nightModeButton.classList.toggle("active");
    document.documentElement.classList.toggle("dark-mode");
  });
}

// setTimeout(() => {
//   const flashes = document.querySelectorAll(".flash");
//   flashes.forEach((flash) => {
//     flash.remove();
//   });
// }, 3000);

const errorFormMessage = document.querySelector(".form-error");

const loginForm = document.querySelector("#login-form");
if (loginForm) {
  loginForm.addEventListener("submit", function (e) {
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();

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

    const memorableInfo = document
      .getElementById("memorable-info")
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

    if (!password) {
      e.preventDefault();
      errorFormMessage.textContent = "Please enter your password!";
      return;
    }

    if (password.length < 10) {
      e.preventDefault();
      errorFormMessage.textContent =
        "Password must be greater than 10 characters";
      return;
    }

    if (!confPassword) {
      e.preventDefault();
      errorFormMessage.textContent = "Please confirm your password!";
      return;
    }

    if (!memorableInfo) {
      e.preventDefault();
      errorFormMessage.textContent = "Please enter your memorable info!";
      return;
    }

    if (password !== confPassword) {
      e.preventDefault();
      errorFormMessage.textContent = "Passwords do not match.";
    }
  });
}

const memorableForm = document.querySelector("#memorable-form");

if (memorableForm) {
  memorableForm.addEventListener("submit", function (e) {
    const email = document.getElementById("email").value.trim();
    const memorableInfo = document
      .getElementById("memorable-info")
      .value.trim();

    if (!email) {
      e.preventDefault();
      errorFormMessage.textContent = "Please enter your email!";
      return;
    }

    if (!memorableInfo) {
      e.preventDefault();
      errorFormMessage.textContent = "Please enter your memorable info!";
      return;
    }
  });
}

const changePasswordForm = document.querySelector("#change-password-form");

if (changePasswordForm) {
  changePasswordForm.addEventListener("submit", function (e) {
    const password = document.getElementById("password").value.trim();
    const confPassword = document
      .getElementById("confirm-password")
      .value.trim();

    if (!password) {
      e.preventDefault();
      errorFormMessage.textContent = "Please enter a new password!";
      return;
    }

    if (!confPassword) {
      e.preventDefault();
      errorFormMessage.textContent = "Please confirm new password!";
      return;
    }

    if (password.length < 10) {
      e.preventDefault();
      errorFormMessage.textContent =
        "Password must be greater than 10 characters!";
      return;
    }

    if (password !== confPassword) {
      e.preventDefault();
      errorFormMessage.textContent = "Password mismatch!";
      return;
    }
  });
}
