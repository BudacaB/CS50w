document.addEventListener('DOMContentLoaded', function() {
    const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun","Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    let localDate = new Date();
    document.querySelector('#local_date').innerHTML = localDate.getDate() + ' ' + monthNames[localDate.getMonth()] + ' ' + localDate.getFullYear();
})