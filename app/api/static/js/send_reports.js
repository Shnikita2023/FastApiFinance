// Отправка отчёта транзакции на email
const sendReportTransaction = () => {
    axios.get('http://127.0.0.1:8000/report/transaction')
    .then(response => {
        if(response.status == 200) {
              alert("Письмо отправлено")
        }
    })
    .catch(error => {
        alert("Ошибка отправки письма")
        console.log(`Ошибка: ${error}`)
    })
}