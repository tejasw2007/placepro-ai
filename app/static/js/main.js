document.addEventListener("DOMContentLoaded", () => {
  const alerts = document.querySelectorAll(".alert");
  alerts.forEach((alert) => {
    setTimeout(() => {
      alert.style.transition = "opacity 0.5s ease, transform 0.5s ease";
      alert.style.opacity = "0";
      alert.style.transform = "translateY(-10px)";
      setTimeout(() => alert.remove(), 500);
    }, 4500);
  });

  const forms = document.querySelectorAll("form");
  forms.forEach((form) => {
    form.addEventListener("submit", () => {
      const submitBtn = form.querySelector('button[type="submit"]');
      if (submitBtn && !submitBtn.disabled) {
        submitBtn.innerText = "Processing...";
        submitBtn.style.opacity = "0.75";
      }
    });
  });
});
