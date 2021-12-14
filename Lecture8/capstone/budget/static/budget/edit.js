document.addEventListener('DOMContentLoaded', function() {
    const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun","Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    let localDateOnLoad = new Date();
    document.querySelector('#local_date').innerHTML = localDateOnLoad.getDate() + ' ' + monthNames[localDateOnLoad.getMonth()] + ' ' + localDateOnLoad.getFullYear();
})

function editExpense(expenseId) {
    document.querySelector(`#expense${expenseId}`).style.display = 'none';
    document.querySelector(`#form${expenseId}`).removeAttribute('hidden');
}

function saveExpense(expenseId, expenseName) {
    console.log(expenseId);
    console.log(expenseName);
    let updatedExpense = document.querySelector(`#input${expenseId}`).value;
    fetch(`/edit/${expenseName}?id=${expenseId}`, {
        method: 'PUT',
        body: JSON.stringify({
            amount: updatedExpense
        })
      })
      .then(response => response.json())
      .then(result => {
        document.querySelector(`#expense${expenseId}`).innerHTML = `$ ${result.updatedExpense}`;
        document.querySelector(`#expense${expenseId}`).style.display = 'block';
        document.querySelector(`#form${expenseId}`).hidden = true;
      })
      .catch(error => console.log('Error', error));
}