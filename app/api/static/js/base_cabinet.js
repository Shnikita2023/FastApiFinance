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

// Функция для получение всех категории финансов при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
        const allCategory = document.getElementById('category')
        fetch('/category/all')
            .then(response => response.json())
            .then(categories => {
                categories.forEach(category => {
                    const option = document.createElement('option');
                    option.textContent = category.name
                    allCategory.appendChild(option)
                })
            })
})


// Получаем форму по id
const formFinance = document.getElementById("form_finance");

formFinance.addEventListener('submit', event => {
  event.preventDefault()  // отменяем стандартное поведение формы

//  async function fetchData(category) {
//    const response = await fetch('http://127.0.0.1:8000/category/?category_name=' + category)
//    const data = await response.json()
//    return data.id
//
//  };

  const formData = new FormData(event.target) // Создаём новую форму с помощью метода event
  const amount = formData.get('amount')
  const category = formData.get('category')
  const description = formData.get('description')
  const type = formData.get('type')

   data_expense = {
            "amount": amount,
            "description": description,
            "type": type,
            "category": category
   }

  fetch("http://127.0.0.1:8000/expense/?category_name=" + category, {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(data_expense)
    })
    .then(response => {
          if(response.status == 200) {  // если ответ не содержит ошибку
                console.log(response.json())
          }
    })
    .catch(error => console.log(`Ошибка: ${error}`));







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
})