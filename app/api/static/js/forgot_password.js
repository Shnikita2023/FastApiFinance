// Сброс пароля
const form = document.getElementById('form_forgot');

form.addEventListener('submit', event => {
    event.preventDefault();

    const formData = new FormData();
    formData.set('email', form.elements.email.value);

    axios.post(
        '/auth/forgot-password',
        formData,
        {
            headers: {
                'Content-Type': 'application/json',
            },
        },
    )
    .then(response => {
        if (response.status == 202) {
              alert("Отправлено письмо на почту, для сброса пароля")
              return window.location.href = '/base';
        }
    })
    .catch(error => {
        alert("Неверный адрес почты")
        console.log(`Ошибка запроса: ${error}`);
    })

});