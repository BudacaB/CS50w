const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun","Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

let dateRefresh = null;
let foodEditUrl;
let billsEditUrl;
let transportEditUrl;
let funEditUrl;

document.addEventListener('DOMContentLoaded', function() {
    let localDateOnLoad = new Date();
    let localDateFormatted = localDateOnLoad.getFullYear() + '-' + (localDateOnLoad.getMonth() + 1) + '-' + localDateOnLoad.getDate();
    document.querySelector('#local_date').innerHTML = localDateOnLoad.getDate() + ' ' + monthNames[localDateOnLoad.getMonth()] + ' ' + localDateOnLoad.getFullYear();
    // set date for stats
    document.querySelector('#food_date').value = localDateFormatted;
    document.querySelector('#bill_date').value = localDateFormatted;
    document.querySelector('#transport_date').value = localDateFormatted;
    document.querySelector('#fun_date').value = localDateFormatted;
    // set date for edits
    foodEditUrl = document.querySelector('#food_edit').href;
    billsEditUrl = document.querySelector('#bills_edit').href;
    transportEditUrl = document.querySelector('#transport_edit').href;
    funEditUrl = document.querySelector('#fun_edit').href;
    document.querySelector('#food_edit').href = foodEditUrl + `?date=${localDateFormatted}`;
    document.querySelector('#bills_edit').href = billsEditUrl + `?date=${localDateFormatted}`;
    document.querySelector('#transport_edit').href = transportEditUrl + `?date=${localDateFormatted}`;
    document.querySelector('#fun_edit').href = funEditUrl + `?date=${localDateFormatted}`;
    getPercentages();
    // keep updating the dates
    dateRefresh = setInterval(function(){ 
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
            getPercentages(null);
        }
    }, 1000);
    dateRefresh;

    document.querySelector('#date_form_day').addEventListener("click", function(event) {
        event.preventDefault();
    });

    document.querySelector('#date_form_interval').addEventListener("click", function(event) {
        event.preventDefault();
    });
})

function addExpense(expense, date, expenseType) {
    fetch('/', {
        method: 'POST',
        body: JSON.stringify({
            type: expenseType,
            expense: parseInt(expense),
            date: date
        })
    })
    .then(response => getPercentages(date))
    .catch(error => console.log('Error', error));
    document.querySelector(`#${expenseType}_expense`).value = '';
}

function getPercentages(date){
    let formattedLocalDate;
    if (date == null) {
        let localDate = new Date();
        formattedLocalDate = localDate.getFullYear() + '-' + (localDate.getMonth() + 1) + '-' + localDate.getDate();
    } else {
        formattedLocalDate = date;
    }
    fetch(`/stats/${formattedLocalDate}`)
    .then(response => response.json())
    .then(result => {
        document.querySelector('#food_stats').innerHTML = result.food;
        document.querySelector('#bills_stats').innerHTML = result.bills;
        document.querySelector('#transport_stats').innerHTML = result.transport;
        document.querySelector('#fun_stats').innerHTML = result.fun;
    })
}

function getDateDay() {
    const regex = /^\d{2}\/\d{2}\/\d{4}$/;
    if (regex.test(document.querySelector('#date_picker_day').value)) {
        document.querySelector('#day_go').removeAttribute("disabled", "");
        return document.querySelector('#date_picker_day').value;
    } else {
        document.querySelector('#day_go').setAttribute("disabled", "");
    } 
}

function getDateStart() {
    return document.querySelector('#date_picker_start').value;
}

function getDateEnd() {
    return document.querySelector('#date_picker_end').value;
}

function changeDate() {
    clearInterval(dateRefresh);
    const date = getDateDay();
    const splitDate = date.split('/');
    const formattedDate = splitDate[2] + '-' + splitDate[0] + '-' + splitDate[1];
    const headerFormattedDate = splitDate[1] + ' ' + monthNames[(splitDate[0] - 1)] + ' ' + splitDate[2];
    document.querySelector('#local_date').innerHTML = headerFormattedDate;
    // set date for stats
    document.querySelector('#food_date').value = formattedDate;
    document.querySelector('#bill_date').value = formattedDate;
    document.querySelector('#transport_date').value = formattedDate;
    document.querySelector('#fun_date').value = formattedDate;
    // set date for edits
    document.querySelector('#food_edit').href = foodEditUrl + `?date=${formattedDate}`;
    document.querySelector('#bills_edit').href = billsEditUrl + `?date=${formattedDate}`;
    document.querySelector('#transport_edit').href = transportEditUrl + `?date=${formattedDate}`;
    document.querySelector('#fun_edit').href = funEditUrl + `?date=${formattedDate}`;
    getPercentages(formattedDate);
}

