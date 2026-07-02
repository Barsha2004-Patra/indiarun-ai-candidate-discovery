document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("searchForm");
    const overlay = document.getElementById("loadingOverlay");

    const loadingMessages = [
        "Parsing Job Description...",
        "Extracting Required Skills...",
        "Generating Embeddings...",
        "Searching 100,000+ Candidates...",
        "Computing Similarity Scores...",
        "Ranking Candidates...",
        "Generating AI Recruiter Insights...",
        "Almost Done..."
    ];

    let loadingIndex = 0;

    if (form) {

        form.addEventListener("submit", function () {

            overlay.style.display = "flex";

            const loadingText = document.getElementById("loadingText");

            loadingText.textContent = loadingMessages[0];

            const interval = setInterval(function () {

                loadingIndex++;

                if (loadingIndex < loadingMessages.length) {

                    loadingText.textContent = loadingMessages[loadingIndex];

                } else {

                    clearInterval(interval);

                }

            }, 700);

        });

    }

    animateCounters();

});


function animateCounters() {

    const cards = document.querySelectorAll(".dashboard-card span");

    if (cards.length < 4) return;

    animateNumber(cards[0], 100000, "+", 1200);

    animateNumber(
        cards[1],
        parseFloat(cards[1].textContent),
        "%",
        1200
    );

    animateNumber(
        cards[2],
        parseInt(cards[2].textContent),
        "",
        1000
    );

}


function animateNumber(element, target, suffix = "", duration = 1000) {

    let start = 0;

    const increment = target / (duration / 16);

    function update() {

        start += increment;

        if (start >= target) {

            if (suffix === "%") {

                element.textContent = target.toFixed(1) + "%";

            }
            else if (suffix === "+") {

                element.textContent =
                    Number(target).toLocaleString() + "+";

            }
            else {

                element.textContent = Math.round(target);

            }

            return;

        }

        if (suffix === "%") {

            element.textContent = start.toFixed(1) + "%";

        }
        else if (suffix === "+") {

            element.textContent =
                Math.round(start).toLocaleString() + "+";

        }
        else {

            element.textContent = Math.round(start);

        }

        requestAnimationFrame(update);

    }

    requestAnimationFrame(update);

}