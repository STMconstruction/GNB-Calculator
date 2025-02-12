<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $name = htmlspecialchars($_POST["user_name"]);
    $phone = htmlspecialchars($_POST["contact_phone"]);
    $length = htmlspecialchars($_POST["drill_length"]);
    $diameter = htmlspecialchars($_POST["pipe_diameter"]);

    // Email, на который отправлять заявки
    $to = "provider@example.com"; // Замените на свою почту
    $subject = "Новая заявка на бурение";
    
    $message = "
    Имя: $name

    Телефон: $phone

    Длина бурения: $length м

    Диаметр трубы: $diameter мм

    ";
    
    $headers = "From: no-reply@example.com" . "\r\n" .
               "Reply-To: $phone" . "\r\n" .
               "Content-Type: text/plain; charset=UTF-8";

    if (mail($to, $subject, $message, $headers)) {
        echo "Спасибо! Ваша заявка отправлена.";
    } else {
        echo "Ошибка при отправке заявки.";
    }
}
?>
