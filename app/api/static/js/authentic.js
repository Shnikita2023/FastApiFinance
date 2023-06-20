// Получаем форму по id
const form = document.getElementById("form_auth");


form.addEventListener('submit', event => {
  event.preventDefault();  // отменяем стандартное поведение формы

// Определяем функцию для обработки отправки формы
//const handleSubmit = (event) => {
//  // Не отправляем форму стандартным способом
//  event.preventDefault();

  // Получаем данные формы
  const formData = new FormData(event.target);

  // Создаем пустой объект для JSON
  const data = {};

  // Заполняем объект данными формы
  for (const [key, value] of formData.entries()) {
    data[key] = value;
  }

  // Отправляем данные на сервер
  fetch("/auth/jwt/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(json => {
    const successMessage = document.createElement('p');
            successMessage.innerHTML = 'Вы успешно авторизованны!';
            form.appendChild(successMessage);
            window.location.href = 'https://www.youtube.com'; // Переход на другую страницу

        })
    .catch(error => console.error(error));
        // В случае ошибки выводим сообщение в консоль
  });


