document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("submitButton").addEventListener("click", function (event) {
        event.preventDefault();  // Останавливаем стандартную отправку формы

        let data = {
            name: document.getElementById("user_name").value,
            phone: document.getElementById("contact_phone").value,
            email: document.getElementById("email").value,
            drill_length: document.getElementById("drill_length").value,
            pipe_diameter: document.getElementById("pipe_diameter").value
        };

        fetch("https://gnb-calculator.onrender.com/submit", {  // Убедись, что URL верный
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            console.log("Ответ сервера:", data);
            alert("✅ Заявка отправлена!");
        })
        .catch(error => {
            console.error("Ошибка:", error);
            alert("❌ Ошибка при отправке!");
        });
    });
});

