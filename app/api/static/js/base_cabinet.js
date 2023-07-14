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

// Функция выбора категории вкладки "Мой кабинет"
document.addEventListener('DOMContentLoaded', function() {
    const accountButton = document.querySelector('.account-button');
    const dropdownContent = document.querySelector('.dropdown-content');

    accountButton.addEventListener('click', function() {
        dropdownContent.classList.toggle('show');
    });

    window.addEventListener('click', function(event) {
        if (!event.target.matches('.account-button')) {
            if (dropdownContent.classList.contains('show')) {
                dropdownContent.classList.remove('show');
            }
        }
    });
})


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
            console.log("Ошибка");
          });

  } else {
    balanceDiv.style.display = 'none';
  }
};




// Отправка обновленных данных пользователя
const editButton = document.querySelector('.edit-button');
const modal = document.querySelector('#modal');
const closeButton = document.querySelector('.close');
const editForm = document.querySelector('#edit-form');

editButton.addEventListener('click', () => {
    modal.style.display = 'block';
});

closeButton.addEventListener('click', () => {
modal.style.display = 'none';
});

editForm.addEventListener('submit', (e) => {
    e.preventDefault();

    const firstName = document.querySelector('#first-name').value;
    const lastName = document.querySelector('#last-name').value;
    const email = document.querySelector('#email').value;
    const username = document.querySelector('#username').value;


    // Отправка данных в БД
    fetch('/edit-data', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json',
        },
        body: JSON.stringify({
        firstName,
        lastName,
        email,
        username
        }),
    })
        .then((response) => response.json())
            .then((data) => {
                console.log('Данные успешно отправлены и сохранены');
                console.log(data);
                modal.style.display = 'none';
            // Дополнительные действия, если требуется после сохранения данных
            })
            .catch((error) => {
                console.error('Ошибка при отправке данных:', error);
            });
});





  // Получение данных о пользователе через библиотеку axios
//  axios.get(
//        'http://127.0.0.1:8000/authentic/me', {
//        headers: {
//            Cookie: localStorage.getItem('access_token')
//        },
//  })
//  .then((response) => {
//        const user = response.data
//        const idUser = user.id
//  })
//  .catch((error) => console.log(error))
//
//
//  data = {
//          "amount": amount,
//          "description": description,
//          "user_id": idUser,
//          "category_id": idCategory
//  }
//
//  // Отправка данных с расходами на API
//  fetch("http://127.0.0.1:8000/expense/add", {
//        method: "POST",
//        headers: {
//          "Content-Type": "application/json"
//        },
//        body: JSON.stringify(data)
//  })
//  .then(response => {
//        if(response.status == 200) {  // если ответ содержит ошибку
//              console.log(response.json())
//        }
//  })
//  .catch(error => console.log(`Ошибка: ${error}`));
