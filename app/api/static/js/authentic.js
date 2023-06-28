// Получаем форму по id
//const form = document.getElementById("form_auth");
//
//
//form.addEventListener("submit", event => {
//  event.preventDefault();  // отменяем стандартное поведение формы
//
////
////  const formData = new FormData();
////  formData.set('username', 'string');
////  formData.set('password', 'string');
////    form.elements.password.value
//  // Отправляем данные на сервер
//  fetch("http://127.0.0.1:8000/auth/jwt/login", {
//    method: "POST",
//    headers: {
//      'Content-Type': 'multipart/form-data',
//    },
//    body: new FormData(form)
//  })
//  .then((response) => console.log(response))
//  .catch(error => console.log(`Ошибка: ${error}`))
//  // В случае ошибки выводим сообщение в консоль
//});

const form = document.getElementById('form_auth');
form.addEventListener('submit', event => {
       event.preventDefault();

       const formData = new FormData();
       formData.set('username', form.elements.username.value);
       formData.set('password', form.elements.password.value);

       axios.post(
           '/auth/jwt/login',
           formData,
           {
               headers: {
                   'Content-Type': 'multipart/form-data',
               },
           },
       )
       .then(response => {
           if (response.status == 204) {
                return window.location.href = '/authentic/cabinet';
           }
       })
       .catch((error) => console.log(`Ошибка запроса: ${error}`));

});