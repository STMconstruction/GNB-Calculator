document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("calculateButton").addEventListener("click", function (event) {
        event.preventDefault();  // Останавливаем стандартное поведение кнопки

        let data = {
            name: document.getElementById("user_name").value,
            phone: document.getElementById("contact_phone").value,
            email: "gnb-client@mail.ru",  // Укажи email клиента
            drill_length: document.getElementById("drill_length").value,
            pipe_diameter: document.getElementById("pipe_diameter").value
        };

        fetch("https://gnb-calculator.onrender.com/submit", {  // Отправка данных на сервер
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            console.log("Ответ сервера:", data);
            alert("✅ Заявка отправлена! Данные пришли вам на почту.");
        })
        .catch(error => {
            console.error("Ошибка:", error);
            alert("❌ Ошибка при отправке!");
        });
    });
});

