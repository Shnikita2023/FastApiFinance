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