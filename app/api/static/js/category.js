// Добавление новой категории в БД
const FormCategory = document.getElementById("form_category");

FormCategory.addEventListener('submit', event => {
  event.preventDefault()  // отменяем стандартное поведение формы


  const formData = new FormData(event.target) // Создаём новую форму с помощью метода event
  const name = formData.get('name')
  const description = formData.get('description')

  data_category = {
            "name": name,
            "description": description,
  }

  axios.post(
             'http://127.0.0.1:8000/category/add',
             data_category,
             {
                 headers: {
                     'Content-Type': 'application/json',
                 },
             },
         )
         .then(response => {
             if (response.status == 200) {
                  alert("Категория добавлена");
             }
         })
         .catch((error) => console.log(`Ошибка запроса: ${error}`));

})