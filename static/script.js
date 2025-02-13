document.getElementById("calculateButton").addEventListener("click", function () {
    const userName = document.getElementById("user_name").value;
    const contactPhone = document.getElementById("contact_phone").value;
    const drillLength = parseFloat(document.getElementById("drill_length").value);
    const pipeDiameter = parseInt(document.getElementById("pipe_diameter").value);

    if (!userName || !contactPhone || !drillLength || !pipeDiameter) {
        alert("Пожалуйста, заполните все поля!");
        return;
    }

    // Логика расчета стоимости по таблице
    let pricePerMeter = 0;

    if (drillLength < 60) {
        if (pipeDiameter <= 100) {
            pricePerMeter = 15000;
        } else if (pipeDiameter <= 200) {
            pricePerMeter = 17000;
        } else if (pipeDiameter <= 315) {
            pricePerMeter = 18000;
        }
    } else {
        if (pipeDiameter <= 100) {
            pricePerMeter = 10000;
        } else if (pipeDiameter <= 200) {
            pricePerMeter = 12000;
        } else if (pipeDiameter <= 315) {
            pricePerMeter = 13000;
        }
    }

    const totalCost = drillLength * pricePerMeter;

    // Вывод результата
    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = `<h3>Расчетная стоимость: ${totalCost.toLocaleString()} тг.</h3>`;

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

