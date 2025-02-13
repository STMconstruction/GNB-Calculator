document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("calculateButton").addEventListener("click", function (event) {
        event.preventDefault();  // Останавливаем стандартное поведение кнопки

        let name = document.getElementById("user_name").value;
        let phone = document.getElementById("contact_phone").value;
        let email = document.getElementById("user_email").value;
        let drill_length = parseFloat(document.getElementById("drill_length").value);
        let pipe_diameter = parseInt(document.getElementById("pipe_diameter").value);

        if (!name || !phone || !email || isNaN(drill_length)) {
            alert("⚠️ Пожалуйста, заполните все поля!");
            return;
        }

        // Формула расчета стоимости
        let pricePerMeter = pipe_diameter <= 100 ? 1000 : pipe_diameter <= 200 ? 1500 : 2000;
        let totalCost = drill_length * pricePerMeter;

        // Вывод расчета на страницу
        document.getElementById("result").innerHTML = `<h3>Предварительная стоимость: ${totalCost} ₽</h3>`;

        // Формируем данные для отправки на сервер
        let data = {
            name: name,
            phone: phone,
            email: email,
            drill_length: drill_length,
            pipe_diameter: pipe_diameter,
            total_cost: totalCost
        };

        // Отправляем данные на сервер Flask
        fetch("https://gnb-calculator.onrender.com/submit", {  
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            console.log("Ответ сервера:", data);
            alert("✅ Расчет выполнен и данные отправлены на почту!");
        })
        .catch(error => {
            console.error("Ошибка:", error);
            alert("❌ Ошибка при отправке данных!");
        });
    });
});

