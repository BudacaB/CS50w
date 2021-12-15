document.addEventListener('DOMContentLoaded', function() {
    const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun","Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    let splitDate = document.querySelector('#edit_date').innerHTML.split('-')
    console.log(parseInt(splitDate[1]))
    document.querySelector('#edit_date').innerHTML = splitDate[2] + ' ' + monthNames[parseInt(splitDate[1]) - 1] + ' ' + splitDate[0]
})

function editExpense(expenseId) {
    document.querySelector(`#expense${expenseId}`).style.display = 'none';
    document.querySelector(`#form${expenseId}`).removeAttribute('hidden');
}

function saveExpense(expenseId, expenseName) {
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

function deleteExpense(expenseId, expenseName) {
    fetch(`/edit/${expenseName}?id=${expenseId}`, {
        method: 'DELETE'
      })
      .then(response => {
          if (response.status === 204) {
            document.querySelector(`#card${expenseId}`).remove()
            document.querySelector(`#br${expenseId}`).remove()
          }
      })
      .catch(error => console.log('Error', error));
}