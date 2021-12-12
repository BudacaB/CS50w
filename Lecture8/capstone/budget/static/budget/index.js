document.addEventListener('DOMContentLoaded', function() {
    const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun","Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    let localDate = new Date();
    document.querySelector('#local_date').innerHTML = localDate.getDate() + ' ' + monthNames[localDate.getMonth()] + ' ' + localDate.getFullYear();
    document.querySelector('#food_date').value = localDate.getFullYear() + '-' + (localDate.getMonth() + 1) + '-' + localDate.getDate();
    document.querySelector('#bill_date').value = localDate.getFullYear() + '-' + (localDate.getMonth() + 1) + '-' + localDate.getDate();
    document.querySelector('#transport_date').value = localDate.getFullYear() + '-' + (localDate.getMonth() + 1) + '-' + localDate.getDate();
    document.querySelector('#fun_date').value = localDate.getFullYear() + '-' + (localDate.getMonth() + 1) + '-' + localDate.getDate();
    setInterval(function(){ 
        let localDate = new Date();
        document.querySelector('#local_date').innerHTML = localDate.getDate() + ' ' + monthNames[localDate.getMonth()] + ' ' + localDate.getFullYear();
        document.querySelector('#food_date').value = localDate.getFullYear() + '-' + (localDate.getMonth() + 1) + '-' + localDate.getDate();
        document.querySelector('#bill_date').value = localDate.getFullYear() + '-' + (localDate.getMonth() + 1) + '-' + localDate.getDate();
        document.querySelector('#transport_date').value = localDate.getFullYear() + '-' + (localDate.getMonth() + 1) + '-' + localDate.getDate();
        document.querySelector('#fun_date').value = localDate.getFullYear() + '-' + (localDate.getMonth() + 1) + '-' + localDate.getDate();
    }, 1000);
})

