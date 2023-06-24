// Получаем форму по id
const form = document.getElementById("form_auth");


form.addEventListener("submit", event => {
  event.preventDefault();  // отменяем стандартное поведение формы

  // Создаем объект для JSON
  const data = {
      username: form.elements.username.value,
      password: form.elements.password.value,
  };

  // Отправляем данные на сервер
  fetch("/auth/jwt/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      "Accept": "application/json"
    },
    body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(json => {
            console.log(json)
        })

  .catch(error => console.log(`Ошибка: ${error}`))
  // В случае ошибки выводим сообщение в консоль
});



