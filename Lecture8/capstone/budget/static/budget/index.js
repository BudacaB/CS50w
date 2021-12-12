document.addEventListener('DOMContentLoaded', function() {
    const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun","Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    let localDateOnLoad = new Date();
    let localDateFormatted = localDateOnLoad.getFullYear() + '-' + (localDateOnLoad.getMonth() + 1) + '-' + localDateOnLoad.getDate();
    document.querySelector('#local_date').innerHTML = localDateOnLoad.getDate() + ' ' + monthNames[localDateOnLoad.getMonth()] + ' ' + localDateOnLoad.getFullYear();
    // set date for stats
    document.querySelector('#food_date').value = localDateFormatted;
    document.querySelector('#bill_date').value = localDateFormatted;
    document.querySelector('#transport_date').value = localDateFormatted;
    document.querySelector('#fun_date').value = localDateFormatted;
    // set date for edits
    let foodEditUrl = document.querySelector('#food_edit').href;
    let billsEditUrl = document.querySelector('#bills_edit').href;
    let transportEditUrl = document.querySelector('#transport_edit').href;
    let funEditUrl = document.querySelector('#fun_edit').href;
    document.querySelector('#food_edit').href = foodEditUrl + `?date=${localDateFormatted}`;
    document.querySelector('#bills_edit').href = billsEditUrl + `?date=${localDateFormatted}`;
    document.querySelector('#transport_edit').href = transportEditUrl + `?date=${localDateFormatted}`;
    document.querySelector('#fun_edit').href = funEditUrl + `?date=${localDateFormatted}`;
    getPercentages();
    // keep updating the dates
    setInterval(function(){ 
        let localDateUpdated = new Date();
        let localDateFormatted = localDateUpdated.getFullYear() + '-' + (localDateUpdated.getMonth() + 1) + '-' + localDateUpdated.getDate();
        document.querySelector('#local_date').innerHTML = localDateUpdated.getDate() + ' ' + monthNames[localDateUpdated.getMonth()] + ' ' + localDateUpdated.getFullYear();
        // set date for stats
        document.querySelector('#food_date').value = localDateFormatted;
        document.querySelector('#bill_date').value = localDateFormatted;
        document.querySelector('#transport_date').value = localDateFormatted;
        document.querySelector('#fun_date').value = localDateFormatted;
        // set date for edits
        document.querySelector('#food_edit').href = foodEditUrl + `?date=${localDateFormatted}`;
        document.querySelector('#bills_edit').href = billsEditUrl + `?date=${localDateFormatted}`;
        document.querySelector('#transport_edit').href = transportEditUrl + `?date=${localDateFormatted}`;
        document.querySelector('#fun_edit').href = funEditUrl + `?date=${localDateFormatted}`;
        // refresh stats if page was opened since yesterday for example
        if (
            (localDateUpdated.getFullYear() + '-' + localDateUpdated.getMonth() + '-' + localDateUpdated.getDate()).localeCompare(
                localDateOnLoad.getFullYear() + '-' + localDateOnLoad.getMonth() + '-' + localDateOnLoad.getDate()
            ) != 0
        ) {
            getPercentages();
        }
    }, 1000);
})

function getPercentages(){
    let localDate = new Date();
    let formattedLocalDate = localDate.getFullYear() + '-' + (localDate.getMonth() + 1) + '-' + localDate.getDate();
    fetch(`/stats/${formattedLocalDate}`)
    .then(response => response.json())
    .then(result => {
        document.querySelector('#food_stats').innerHTML = result.food;
        document.querySelector('#bills_stats').innerHTML = result.bills;
        document.querySelector('#transport_stats').innerHTML = result.transport;
        document.querySelector('#fun_stats').innerHTML = result.fun;
    })
}
