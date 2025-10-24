document.getElementById("titanicForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());

    // Convertir valores numéricos
    data.Pclass = parseInt(data.Pclass);
    data.Age = Math.round(parseFloat(data.Age));
    data.SibSp = parseInt(data.SibSp);
    data.Parch = parseInt(data.Parch);
    data.FamilySize = data.SibSp + data.Parch + 1;

    // Asignar tarifa automáticamente según la clase
    const fareMap = {1: 512, 2: 73, 3: 0};
    data.Fare = fareMap[data.Pclass];

    // Validaciones simples
    if (data.Age < 0 || data.Age > 100) { alert("Edad inválida."); return; }
    if (data.SibSp < 0 || data.SibSp > 10) { alert("Número de hermanos/pareja inválido."); return; }
    if (data.Parch < 0 || data.Parch > 10) { alert("Número de padres/hijos inválido."); return; }

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const res = await fetch("/predict/", {
        method: "POST",
        headers: { 
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken
        },
        body: JSON.stringify(data),
    });

    const result = await res.json();
    const resultText = document.getElementById("resultText");

    resultText.style.opacity = 0;
    setTimeout(() => {
        resultText.textContent = result.prediction || result.detail;
        resultText.style.opacity = 1;
    }, 200);
});
