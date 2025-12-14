document.addEventListener("DOMContentLoaded", function() {
    console.log("Django Blog JS loaded successfully!");

    // Auto-dismiss Django messages after 5 seconds
    const messages = document.querySelectorAll(".messages li, .alert");
    messages.forEach(msg => {
        setTimeout(() => {
            msg.style.transition = "opacity 0.5s ease";
            msg.style.opacity = "0";
            setTimeout(() => msg.remove(), 500);
        }, 5000);
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener("click", function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute("href"));
            if (target) {
                target.scrollIntoView({ behavior: "smooth" });
            }
        });
    });

    // Add click feedback to buttons
    document.querySelectorAll(".btn").forEach(button => {
        button.addEventListener("click", () => {
            button.classList.add("active");
            setTimeout(() => button.classList.remove("active"), 150);
        });
    });
});
