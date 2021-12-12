document.addEventListener('DOMContentLoaded', function() {
    const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun","Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    let localDateOnLoad = new Date();
    document.querySelector('#local_date').innerHTML = localDateOnLoad.getDate() + ' ' + monthNames[localDateOnLoad.getMonth()] + ' ' + localDateOnLoad.getFullYear();
})

function editExpense(expenseId, expenseName) {
    document.querySelector(`#expense${expenseId}`).style.display = 'none';
    document.querySelector(`#form${expenseId}`).removeAttribute('hidden');
}

function saveExpense(expenseId) {
    let updatedExpense = document.querySelector(`#input${expenseId}`).value;
    console.log(updatedExpense);
}