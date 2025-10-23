document.getElementById("titanicForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());

     data.Pclass = parseInt(data.Pclass);
    data.Age = parseFloat(data.Age);
    data.SibSp = parseInt(data.SibSp);
    data.Parch = parseInt(data.Parch);
    data.Fare = parseFloat(data.Fare);
    data.IsAlone = parseInt(data.IsAlone);
    data.FamilySize = data.SibSp + data.Parch + 1;

    const res = await fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });

    const result = await res.json();
    const text = document.getElementById("resultText");
    const ship = document.getElementById("ship");

    if (result.prediction) {
        text.textContent = result.prediction;

        if (result.prediction.includes("Sobrevive")) {
            ship.style.left = "85%";
            ship.style.top = "20px";
            text.style.color = "#6abf69";
        } else {
            ship.style.left = "45%";
            ship.style.top = "60px";
            text.style.color = "#d64c4c";
        }
    } else {
        text.textContent = "Error en la predicción.";
        text.style.color = "gray";
    }
});
