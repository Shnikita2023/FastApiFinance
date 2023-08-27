// Функция для выхода с аккаунта
const logoutUser = () => {
    axios.post('/auth/jwt/logout',
        null,
        {
            headers: {
                'Cookie': `fastapiusersauth=${localStorage.getItem('access_token')}`,
            },
        }
    )
    .then(response => {
        if(response.status == 204) {
            return window.location.href = '/base/'
        }
    })
    .catch(error => console.log(`Ошибка: ${error}`))

};


// Получение баланса пользователя с БД и вывод на экран
const myBalance = () => {
  const balanceDiv = document.getElementById('balanceDiv');
  if (balanceDiv.style.display === 'none') {
    balanceDiv.style.display = 'block';
    axios.get('/balance/')
          .then(response => {
            if (response.status == 200) {
                const balance = response.data.total_balance + 'руб'
                balanceDiv.textContent = balance;
            }
          })
          .catch(error => {
            console.log("Ошибка получение баланса");
          });

  } else {
    balanceDiv.style.display = 'none';
  }
};


// Отправка обновленных данных пользователя на сервер
const editButton = document.querySelector('.edit-button');
const modal = document.querySelector('#modal');
const closeButton = document.querySelector('.close');
const editForm = document.querySelector('#edit-form');

// Функция отображения модального окна
function showModal() {
    modal.style.display = 'block';
}

// Функция закрытия модального окна
function closeModal() {
   modal.style.display = 'none';
}

// Функция обработки отправки формы
function handleSubmit(e) {
    e.preventDefault();

    const firstName = document.querySelector('#first-name').value;
    const lastName = document.querySelector('#last-name').value;
    const email = document.querySelector('#email').value;
    const userName = document.querySelector('#username').value;
    const password = document.querySelector('#password').value;

        const newDataUser = {
            "email": email,
            "password": password,
            "username": userName,
            "last_name": lastName,
            "first_name": firstName,
        };

        // Отправка обновлённых данных в БД
    fetch('http://127.0.0.1:8000/users/me', {
        method: 'PATCH',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(newDataUser),
    })
        .then((response) => {
            if(response.status == 200) {  // если ответ не содержит ошибку
                alert('Данные успешно отправлены и сохранены');
                modal.style.display = 'none';
            } else {
                console.log(response);
                response.json()
                    .then(data => {
                        const errorMessage = data.detail;
                        alert(errorMessage);
                    });
            }
        })
        .catch((error) => {
            console.error('Ошибка при отправке данных:', error);
        });
}

// Добавление обработчиков событий
editButton.addEventListener('click', showModal);
closeButton.addEventListener('click', closeModal);
editForm.addEventListener('submit', handleSubmit);
