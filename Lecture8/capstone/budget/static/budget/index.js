document.addEventListener('DOMContentLoaded', function() {
    let utc = document.querySelector('#utc').innerHTML;
    let localDate = new Date(`${utc} UTC`).toISOString().slice(0, 10);
    document.querySelector('#local_date').innerHTML = localDate;
})