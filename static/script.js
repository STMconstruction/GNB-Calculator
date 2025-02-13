document.getElementById("calculateButton").addEventListener("click", function () {
    const userName = document.getElementById("user_name").value;
    const contactPhone = document.getElementById("contact_phone").value;
    const drillLength = parseFloat(document.getElementById("drill_length").value);
    const pipeDiameter = parseInt(document.getElementById("pipe_diameter").value);

    if (!userName || !contactPhone || !drillLength || !pipeDiameter) {
        alert("Пожалуйста, заполните все поля!");
        return;
    }

    // Логика расчета стоимости
    const pricePerMeter = pipeDiameter * 10;
    const totalCost = drillLength * pricePerMeter;

    // Вывод результата
    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = `<h3>Расчетная стоимость: ${totalCost} руб.</h3>`;

    // Отправка данных на сервер
    fetch("/submit", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name: userName,
            phone: contactPhone,
            drill_length: drillLength,
            pipe_diameter: pipeDiameter,
            total_cost: totalCost
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Расчет выполнен и данные отправлены!");
        } else {
            alert("Ошибка при отправке данных.");
        }
    })
    .catch(error => {
        console.error("Ошибка:", error);
        alert("Ошибка при отправке данных.");
    });
});

