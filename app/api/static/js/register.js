// Получаем форму по id
const form = document.getElementById("myform");


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
  fetch("/auth/register", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(json => {
    const successMessage = document.createElement('p');
            successMessage.innerHTML = 'Вы успешно зарегистрированы!';
            form.appendChild(successMessage);
            setTimeout(() => {
                window.location.href = '/base'; // Переход на другую страницу
            }, 5000); // Ждем 3 секунды, прежде чем перенаправить пользователя
        })
    .catch(error => console.error(error));
        // В случае ошибки выводим сообщение в консоль
  });


