document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ script.js загружен!");

    // Получаем элементы формы и кнопки
    const form = document.getElementById("calcForm");
    const resultBox = document.getElementById("result");
    const button = document.getElementById("calculateButton");

    if (!form) {
        console.error("❌ Ошибка: Форма не найдена!");
        return;
    }

    if (!button) {
        console.error("❌ Ошибка: Кнопка не найдена!");
        return;
    }

    // Добавляем обработчик клика по кнопке
    button.addEventListener("click", function () {
        console.log("🔘 Кнопка нажата, расчет запущен!");

        const name = document.getElementById("user_name").value.trim();
        const phone = document.getElementById("contact_phone").value.trim();
        const length = parseFloat(document.getElementById("drill_length").value);
        const diameter = parseInt(document.getElementById("pipe_diameter").value);

        if (!name || !phone) {
            alert("❌ Введите имя и телефон!");
            return;
        }

        if (!length || length <= 0) {
            alert("❌ Введите корректную длину бурения!");
            return;
        }

        console.log(`📊 Данные: Имя=${name}, Телефон=${phone}, Длина=${length}, Диаметр=${diameter}`);

        // Расчет стоимости
        const cost = calculateCost(length, diameter);

        // Вывод результата
        showCalculationResults(name, length, diameter, cost);

        // Отправка данных на сервер
        sendDataToServer({ name, phone, length, diameter, cost });
    });

    function calculateCost(length, diameter) {
        let rate = 0;

        if (length <= 60) {
            if (diameter <= 100) rate = 15000;
            else if (diameter <= 200) rate = 17000;
            else rate = 18000;
        } else {
            if (diameter <= 100) rate = 10000;
            else if (diameter <= 200) rate = 12000;
            else rate = 13000;
        }

        return length * rate;
    }

    function showCalculationResults(name, length, diameter, cost) {
        resultBox.innerHTML = `
            <h3>📌 Предварительный расчет</h3>
            <p><strong>${name}</strong></p>
            <p>Длина бурения: <strong>${length} м</strong></p>
            <p>Диаметр трубы: <strong>${diameter} мм</strong></p>
            <p>💰 Примерная стоимость: <strong>${cost.toLocaleString()} тенге</strong></p>
        `;
        resultBox.style.display = "block";
    }

    function sendDataToServer(data) {
        fetch("/submit", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        })
            .then(response => response.json())
            .then(result => {
                if (result.success) {
                    alert("✅ Заявка успешно отправлена!");
                } else {
                    alert("❌ Ошибка отправки!");
                }
            })
            .catch(error => console.error("Ошибка:", error));
    }
});

