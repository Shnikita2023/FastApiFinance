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

            .catch(error => console.log(`Ошибка: ${error}`));
})


// Получаем форму по id и добавляем транзакцию
const formFinance = document.getElementById("form_finance");

formFinance.addEventListener('submit', event => {
  event.preventDefault()  // отменяем стандартное поведение формы


  const formData = new FormData(event.target) // Создаём новую форму с помощью метода event
  const amount = formData.get('amount')
  const category = formData.get('category')
  const comment = formData.get('comment')
  const type_transaction = formData.get('type_transaction')


  data_expense = {
            "amount": amount,
            "comment": comment,
            "type_transaction": type_transaction,
            "category": category
  }

  fetch("/transaction/formation", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(data_expense)
    })
    .then(response => {
          if(response.status == 200) {  // если ответ не содержит ошибку
              alert("Запись добавлена")
          }
    })
    .catch(error => console.log(`Ошибка: ${error}`));

})


