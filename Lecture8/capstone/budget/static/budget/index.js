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
    // making sure to reset the values with 'split' because 'resetAndReload()' might append multiple dates on repeat calling
    foodEditUrl = document.querySelector('#food_edit').href.split('?')[0];
    billsEditUrl = document.querySelector('#bills_edit').href.split('?')[0];
    transportEditUrl = document.querySelector('#transport_edit').href.split('?')[0];
    funEditUrl = document.querySelector('#fun_edit').href.split('?')[0];
    document.querySelector('#food_edit').href = foodEditUrl + `?date=${localDateFormatted}`;
    document.querySelector('#bills_edit').href = billsEditUrl + `?date=${localDateFormatted}`;
    document.querySelector('#transport_edit').href = transportEditUrl + `?date=${localDateFormatted}`;
    document.querySelector('#fun_edit').href = funEditUrl + `?date=${localDateFormatted}`;
    getAmountsAndPercentages();
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
            getAmountsAndPercentages(null);
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
            expense: expense,
            date: date
        })
    })
    .then(response => getAmountsAndPercentages(date))
    .catch(error => console.log('Error', error));
    document.querySelector(`#${expenseType}_expense`).value = '';
}

function getAmountsAndPercentages(date){
    let formattedLocalDate;
    if (date == null || date === '') {
        let localDate = new Date();
        formattedLocalDate = localDate.getFullYear() + '-' + (localDate.getMonth() + 1) + '-' + localDate.getDate();
    } else {
        formattedLocalDate = date;
    }
    fetch(`/stats/${formattedLocalDate}`)
    .then(response => response.json())
    .then(result => {
        let total = result.food + result.bills + result.transport + result.fun;
        document.querySelector('#food_stats').innerHTML = `$${result.food.toFixed(2)} | ${result.food_stats}%`;
        document.querySelector('#bills_stats').innerHTML = `$${result.bills.toFixed(2)} | ${result.bills_stats}%`;
        document.querySelector('#transport_stats').innerHTML = `$${result.transport.toFixed(2)} | ${result.transport_stats}%`;
        document.querySelector('#fun_stats').innerHTML = `$${result.fun.toFixed(2)} | ${result.fun_stats}%`;
        document.querySelector('#total').innerHTML = `Total: $ ${total.toFixed(2)}`;
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

function getDateRange() {
    const regex = /^\d{2}\/\d{2}\/\d{4}$/;
    if (regex.test(document.querySelector('#date_picker_start').value) &&
        regex.test(document.querySelector('#date_picker_end').value)) {
        document.querySelector('#interval_go').removeAttribute("disabled", "");
        return document.querySelector('#date_picker_start').value + '-' + document.querySelector('#date_picker_end').value;
    } else {
        document.querySelector('#interval_go').setAttribute("disabled", "");
    } 
}

function useDateRange() {
    // not moving away from the selected dates
    clearInterval(dateRefresh);
    document.querySelector('#refresh').hidden = true;
    document.querySelector('#date_picker_day').value = '';
    // remove editing capabilities for a range - works only for one day
    document.querySelector('#food_edit').removeAttribute('href');
    document.querySelector('#bills_edit').removeAttribute('href');
    document.querySelector('#transport_edit').removeAttribute('href');
    document.querySelector('#fun_edit').removeAttribute('href');
    const dateRange = getDateRange();
    const startDateRaw = dateRange.split('-')[0].split('/');
    const endDateRaw = dateRange.split('-')[1].split('/');
    const startDate = startDateRaw[2] + '-' + startDateRaw[0] + '-' + startDateRaw[1];
    const endDate = endDateRaw[2] + '-' + endDateRaw[0] + '-' + endDateRaw[1];
    const headerFormattedDate = startDateRaw[1] + ' ' + monthNames[(startDateRaw[0] - 1)] + ' ' + startDateRaw[2] + ' - ' + endDateRaw[1] + ' ' + monthNames[(endDateRaw[0] - 1)] + ' ' + endDateRaw[2];
    document.querySelector('#local_date').innerHTML = headerFormattedDate;
    document.querySelector('#expenses_input').style.display = 'none';
    fetch(`/range?start=${startDate}&end=${endDate}`)
    .then(response => response.json())
    .then(result => {
        document.querySelector('#food_stats').innerHTML = `$${result.food} | ${result.food_stats}%`;
        document.querySelector('#bills_stats').innerHTML = `$${result.bills} | ${result.bills_stats}%`;
        document.querySelector('#transport_stats').innerHTML = `$${result.transport} | ${result.transport_stats}%`;
        document.querySelector('#fun_stats').innerHTML = `$${result.fun} | ${result.fun_stats}%`;
    })
}

function changeDate() {
    // not moving away from the selected date
    clearInterval(dateRefresh);
    document.querySelector('#date_picker_start').value = '';
    document.querySelector('#date_picker_end').value = '';
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
    getAmountsAndPercentages(formattedDate);
}

function resetAndReload() {
    document.querySelector('#expenses_input').style.display = 'block';
    document.querySelector('#date_picker_day').value = '';
    document.querySelector('#date_picker_start').value = '';
    document.querySelector('#date_picker_end').value = '';
    document.querySelector('#refresh').removeAttribute('hidden');
    // restarting the interval via triggering a DOMContentLoaded event
    window.document.dispatchEvent(new Event("DOMContentLoaded", {
        bubbles: true,
        cancelable: true
    }));
}

function refresh() {
    monthNames
    const dateSplit = document.querySelector('#local_date').innerHTML.split(' ');
    const formattedDate = dateSplit[2] + '-' + (monthNames.indexOf(dateSplit[1]) + 1) + '-' + dateSplit[0];
    getAmountsAndPercentages(formattedDate);
}