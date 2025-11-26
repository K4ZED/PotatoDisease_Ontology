async function fetchJson(url) {
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error("Request failed");
    }
    return response.json();
}

function initDiagnoseForm() {
    const form = document.querySelector("form[data-role='diagnose']") || document.querySelector("form");
    if (!form) return;
    if (!form.querySelector("input[name='symptoms']")) return;

    let resultContainer = document.getElementById("diagnose-result");
    if (!resultContainer) {
        resultContainer = document.createElement("div");
        resultContainer.id = "diagnose-result";
        form.parentNode.insertBefore(resultContainer, form.nextSibling);
    }

    form.addEventListener("submit", async function (event) {
        event.preventDefault();

        const checked = Array.from(form.querySelectorAll("input[name='symptoms']:checked"));
        if (checked.length === 0) {
            resultContainer.innerHTML = "<p>Tidak ada gejala yang dipilih.</p>";
            return;
        }

        const counts = {};
        for (const input of checked) {
            const iri = input.value;
            try {
                const data = await fetchJson("/api/symptom?iri=" + encodeURIComponent(iri));
                const diseases = data.diseases || [];
                for (const d of diseases) {
                    counts[d] = (counts[d] || 0) + 1;
                }
            } catch (e) {
                console.error(e);
            }
        }

        const entries = Object.entries(counts).sort(function (a, b) {
            return b[1] - a[1];
        });

        if (entries.length === 0) {
            resultContainer.innerHTML = "<p>Tidak ditemukan penyakit yang cocok.</p>";
            return;
        }

        const list = document.createElement("ul");
        entries.forEach(function (item) {
            const li = document.createElement("li");
            li.textContent = item[0] + " (skor " + item[1] + ")";
            list.appendChild(li);
        });

        resultContainer.innerHTML = "<h3>Hasil Diagnosa</h3>";
        resultContainer.appendChild(list);
    });
}

document.addEventListener("DOMContentLoaded", function () {
    initDiagnoseForm();
});
