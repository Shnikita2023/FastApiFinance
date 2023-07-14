const form = document.getElementById('form_reset');

form.addEventListener('submit', event => {
    event.preventDefault();

    const formData = new FormData();
    formData.set('token', form.elements.token.value);
    formData.set('password', form.elements.new_password.value);

    axios.post(
        '/auth/reset-password',
        formData,
        {
            headers: {
                'Content-Type': 'application/json',
            },
        },
    )
    .then(response => {
        if (response.status == 200) {
              alert("Новый пароль установлен!")
              return window.location.href = '/base';
        }
    })
    .catch((error) => {
            alert(error.response.data.detail);

       })
});