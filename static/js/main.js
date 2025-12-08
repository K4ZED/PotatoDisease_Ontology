document.addEventListener("DOMContentLoaded", function () {
    var diagnoseForm = document.querySelector(".diagnose-form");
    if (diagnoseForm) {
        var submitButton = diagnoseForm.querySelector(".primary-button");
        diagnoseForm.addEventListener("submit", function () {
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.dataset.originalText = submitButton.textContent;
                submitButton.textContent = "Processing...";
            }
            document.body.classList.add("is-loading");
        });
    }

    var diseaseCards = document.querySelectorAll(".disease-card");
    diseaseCards.forEach(function (card) {
        card.addEventListener("click", function (event) {
            var target = event.target;
            if (target.closest("a") || target.closest("button")) {
                return;
            }
            card.classList.toggle("expanded");
        });
    });

    var links = document.querySelectorAll('a[href^="#"]');
    links.forEach(function (link) {
        link.addEventListener("click", function (event) {
            var href = link.getAttribute("href");
            if (!href || href.length < 2) return;
            var target = document.querySelector(href);
            if (!target) return;
            event.preventDefault();
            target.scrollIntoView({ behavior: "smooth", block: "start" });
        });
    });
});
