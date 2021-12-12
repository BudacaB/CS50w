document.addEventListener('DOMContentLoaded', function() {
    const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun","Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    let localDateOnLoad = new Date();
    document.querySelector('#local_date').innerHTML = localDateOnLoad.getDate() + ' ' + monthNames[localDateOnLoad.getMonth()] + ' ' + localDateOnLoad.getFullYear();
    document.querySelector('#food_date').value = localDateOnLoad.getFullYear() + '-' + (localDateOnLoad.getMonth() + 1) + '-' + localDateOnLoad.getDate();
    document.querySelector('#bill_date').value = localDateOnLoad.getFullYear() + '-' + (localDateOnLoad.getMonth() + 1) + '-' + localDateOnLoad.getDate();
    document.querySelector('#transport_date').value = localDateOnLoad.getFullYear() + '-' + (localDateOnLoad.getMonth() + 1) + '-' + localDateOnLoad.getDate();
    document.querySelector('#fun_date').value = localDateOnLoad.getFullYear() + '-' + (localDateOnLoad.getMonth() + 1) + '-' + localDateOnLoad.getDate();
    getPercentages();
    // keep updating the dates
    setInterval(function(){ 
        let localDateUpdated = new Date();
        document.querySelector('#local_date').innerHTML = localDateUpdated.getDate() + ' ' + monthNames[localDateUpdated.getMonth()] + ' ' + localDateUpdated.getFullYear();
        document.querySelector('#food_date').value = localDateUpdated.getFullYear() + '-' + (localDateUpdated.getMonth() + 1) + '-' + localDateUpdated.getDate();
        document.querySelector('#bill_date').value = localDateUpdated.getFullYear() + '-' + (localDateUpdated.getMonth() + 1) + '-' + localDateUpdated.getDate();
        document.querySelector('#transport_date').value = localDateUpdated.getFullYear() + '-' + (localDateUpdated.getMonth() + 1) + '-' + localDateUpdated.getDate();
        document.querySelector('#fun_date').value = localDateUpdated.getFullYear() + '-' + (localDateUpdated.getMonth() + 1) + '-' + localDateUpdated.getDate();
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
