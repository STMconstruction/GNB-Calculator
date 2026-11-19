const WHATSAPP_NUMBER = "77074878821";
const MAX_LENGTH = 5000;

const phoneInput = document.getElementById("contact_phone");

// Приводит ввод к 11 цифрам, начиная с 7 (8xxx → 7xxx)
function phoneDigits(value) {
    let d = value.replace(/\D/g, "");
    if (d.startsWith("8")) d = "7" + d.slice(1);
    if (d && !d.startsWith("7")) d = "7" + d;
    return d.slice(0, 11);
}

// Маска +7 (7xx) xxx-xx-xx
function formatPhone(d) {
    if (!d) return "";
    let s = "+7";
    if (d.length > 1) s += " (" + d.slice(1, 4);
    if (d.length >= 4) s += ")";
    if (d.length > 4) s += " " + d.slice(4, 7);
    if (d.length > 7) s += "-" + d.slice(7, 9);
    if (d.length > 9) s += "-" + d.slice(9, 11);
    return s;
}

phoneInput.addEventListener("input", function () {
    phoneInput.value = formatPhone(phoneDigits(phoneInput.value));
});

function pricePerMeter(length, diameter) {
    if (length < 60) {
        if (diameter <= 100) return 15000;
        if (diameter <= 200) return 17000;
        return 18000;
    }
    if (diameter <= 100) return 10000;
    if (diameter <= 200) return 12000;
    return 13000;
}

function waLink(text) {
    return "https://wa.me/" + WHATSAPP_NUMBER + "?text=" + encodeURIComponent(text);
}

document.getElementById("calculateButton").addEventListener("click", function () {
    const button = this;
    const userName = document.getElementById("user_name").value.trim();
    const phone = phoneDigits(phoneInput.value);
    const drillLength = parseFloat(document.getElementById("drill_length").value);
    const pipeDiameter = parseInt(document.getElementById("pipe_diameter").value, 10);
    const honeypot = document.getElementById("website").value;

    if (!userName) {
        alert("Введите имя.");
        return;
    }
    if (phone.length !== 11 || phone[1] !== "7") {
        alert("Введите корректный номер: +7 (7xx) xxx-xx-xx");
        return;
    }
    if (!drillLength || drillLength < 1 || drillLength > MAX_LENGTH) {
        alert("Длина бурения должна быть от 1 до " + MAX_LENGTH + " м.");
        return;
    }

    const totalCost = drillLength * pricePerMeter(drillLength, pipeDiameter);
    const costText = totalCost.toLocaleString("ru-RU");

    const waText =
        "Здравствуйте! Хочу заказать ГНБ.\n" +
        "Имя: " + userName + "\n" +
        "Длина: " + drillLength + " м\n" +
        "Диаметр: до " + pipeDiameter + " мм\n" +
        "Расчёт с сайта: " + costText + " тг";

    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = "";
    const h3 = document.createElement("h3");
    h3.textContent = "Расчетная стоимость: " + costText + " тг.";
    const wa = document.createElement("a");
    wa.className = "wa-button";
    wa.href = waLink(waText);
    wa.target = "_blank";
    wa.rel = "noopener";
    wa.textContent = "Обсудить в WhatsApp";
    resultDiv.append(h3, wa);
    document.getElementById("waFloat").href = waLink(waText);

    button.disabled = true;
    fetch("/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            name: userName,
            phone: phone,
            drill_length: drillLength,
            pipe_diameter: pipeDiameter,
            website: honeypot
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Заявка отправлена! Мы свяжемся с вами.");
        } else {
            alert(data.error || "Не удалось отправить заявку. Напишите нам в WhatsApp.");
        }
    })
    .catch(() => {
        alert("Не удалось отправить заявку. Напишите нам в WhatsApp.");
    })
    .finally(() => {
        button.disabled = false;
    });
});
