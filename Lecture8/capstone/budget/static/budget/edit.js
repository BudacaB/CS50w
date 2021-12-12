function editExpense(expenseId, expenseName) {
    document.querySelector(`#expense${expenseId}`).style.display = 'none';
    document.querySelector(`#form${expenseId}`).removeAttribute('hidden');
}

function saveExpense(expenseId) {
    let updatedExpense = document.querySelector(`#input${expenseId}`).value;
    console.log(updatedExpense);
}