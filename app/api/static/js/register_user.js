// Получаем форму по id
const form = document.getElementById("form_register");


form.addEventListener('submit', event => {
  event.preventDefault();  // отменяем стандартное поведение формы

  // Получаем данные формы
  const formData = new FormData(event.target);

  // Создаем пустой объект для JSON
  const data = {};

  // Заполняем объект данными формы
  for (const [key, value] of formData.entries()) {
    data[key] = value;
  }

  // Отправляем данные на сервер
  fetch("/auth/register", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  })
  .then(response => {
    if (!response.ok) {  // если ответ содержит ошибку
          response.json()
            .then(data => {
                const errorMessage = data.detail
                alert(errorMessage)
            })
    }
    return response.json()
  })
  .then(json => {
    const successMessage = document.createElement('p');
            successMessage.innerHTML = 'Вы успешно зарегистрированы!';
            form.appendChild(successMessage);
            setTimeout(() => {
                window.location.href = '/base'; // Переход на другую страницу
            }, 1000); // Ждем 5 секунды, прежде чем перенаправить пользователя
        })
  .catch((error) => console.log(`Ошибка запроса: ${error}`));
});