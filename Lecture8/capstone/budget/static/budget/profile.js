function deleteAccount() {
    if (confirm('Are you sure you want delete the account and lose all data?')) {
        fetch('/profile', {
        method: 'DELETE'
        })
        .then(response => console.log(response))
        .catch(error => console.log('Error', error));
    }
    window.location.href = '/login';
}