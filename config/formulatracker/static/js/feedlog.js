// FEED TOTAL FUNCTION

var table = document.getElementById('feedtable');
var total = 0;

for(var i = 1; i < table.rows.length - 1; i++) {
    total += parseInt(table.rows[i].cells[1].innerHTML);
}

document.getElementById('totalFeed').innerHTML = '<b>' + total + '</b>';

total = total ? total : 0;

// FEED LOG FILTER: Limit the DatePicker to current date

var today = new Date().toISOString().split('T')[0];
document.getElementsByName("dayfilter")[0].setAttribute('max', today);

// FEED RATE CONVERSION 
var conForm = document.getElementById('convertForm')
$( conForm ).on( "submit", function( event ) {
    event.preventDefault();
    let rawLength = jQuery('input[name="feedlength"]').val();
    minutes = rawLength
    console.log(minutes)
    let amount = jQuery('input[name="nextfeedamount"]').val();
    console.log(amount)

    convert = (amount / minutes)
    console.log(convert)
    document.getElementsByName('display')[0].value = convert
});


// PROGRESS BAR FUNCTIONALITY //

// get the user'S goal to then divide by the total feeds taken for the day
var usergoal = document.getElementById('usergoal').innerHTML
console.log(usergoal)
var feedPercentage = parseInt((total / usergoal) * 100);
console.log(feedPercentage)

// Animates, updates the progress bar. Changes color to green "success", once the goal is reached (100%) 
if (usergoal != 0) {
    $('.progress-bar').animate({
        width: feedPercentage + '%',

    }, 500);

    var interval = setInterval(function () {
        if (feedPercentage < 100) {
            $('.progress-bar').html(feedPercentage + '%');
        } else {
            $('#progressBar').removeClass().addClass("progress-bar bg-success progress-bar-striped progress-bar-animated");
            $('.progress-bar').html('100%' + ' - Goal Reached!');
            
            clearInterval(interval)
        }
    }, 500);
} else {
    $('.progress-bar').html(0 + '%');

}

// BAR CHART - FEEDINGS BY DATE
// settings to set defaults to mimic current website styling
Chart.defaults.global.defaultFontFamily = 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", "Liberation Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"';
Chart.defaults.global.defaultFontColor = '#858796';

let select = document.querySelector('#dataFilter');
select.addEventListener('change', showHide);

// HIDES CHARTS THAT ARE CURRENTLY SELECTED
function showHide() {
    let chart = select.options[select.selectedIndex].value + 'BarChart'
    document.querySelectorAll('canvas').forEach(c => {
        c.style.display = (c.id === chart)? 'inherit' : 'none';
    })
}

// Set default of select Tag to the Daily graph
window.addEventListener("load", function () {
    change = $('#daily').val('daily').change();
    showHide(change)
})

// DAILY CHART CONFIGURATION + LABELS & DATA
endpointDaily = '/dailydata/'

$.ajax({
    method: 'GET',
    url: endpointDaily,
    dataType: "json",
    success: function(jsonResponse){
        dates = jsonResponse.labels
        amount = jsonResponse.data
        units = jsonResponse.units
        if (units === 'IMPERIAL') {
            amount = [Math.round(jsonResponse.data / 29.574)]
        } 
        else {
            amount = jsonResponse.data
        }
        setChart()
    },
    error: function(error_data){
        console.log("error")
        console.log(error_data)
    }
})

function setChart(){
    var ctx = document.getElementById('dailyBarChart');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: dates,
                datasets: [{
                    label: "Total Daily Feed Amount",
                    data: amount,
                    backgroundColor: 'rgba(13, 202, 240, 0.2)',
                    borderColor: 'rgba(13, 202, 240, 1)',
                    borderWidth: 1,
                    barThickness: 100,
                }],
            },
            options: {
                responsive: true,
                max: amount,
                scales: {
                    xAxes: [{
                        barPercentage: 0.2
                    }],
                    yAxes: [{
                        ticks:{beginAtZero:true},
                    }]
                },
                title:{
                    display: true,
                    text:"Daily Feed Total",
                    fontSize:20,
                }
            }
        })
}


// WEEKLY CHART CONFIGURATION + LABELS & DATA
endpointWeekly = '/weeklydata/'
$.ajax({
    method: 'GET',
    url: endpointWeekly,
    dataType: "json",
    success: function(jsonResponse){
        dates = jsonResponse.labels
        amount = jsonResponse.data

        setWeeklyChart()
    },
    error: function(error_data){
        console.log("error")
        console.log(error_data)
    }
})

function setWeeklyChart(){
    var ctx = document.getElementById('weeklyBarChart');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: dates,
                datasets: [{
                    label: "Total Weekly Feed Amount",
                    data: amount,
                    backgroundColor: 'rgba(13, 202, 240, 0.2)',
                    borderColor: 'rgba(13, 202, 240, 1)',
                    borderWidth: 1
                }],
            },
            options: {
                responsive: true,
                max: amount,
                scales: {
                    xAxes: [{
                        barPercentage: 1
                    }],
                    yAxes: [{
                        ticks:{beginAtZero:true},
                    }]
                },
                title:{
                    display: true,
                    text:"Totals from Last 7 Days",
                    fontSize:20,
                }
            }
        })
}

// MONTHLY CHART.JS CONFIGURATION + LABELS & DATA
endpoint1 = '/monthdata/'
$.ajax({
    method: 'GET',
    url: endpoint1,
    dataType: "json",
    success: function(jsonResponse){
        dates = jsonResponse.labels
        amount = jsonResponse.data
        setMonthlyChart()
    },
    error: function(error_data){
        console.log("error")
        console.log(error_data)
    }
})

function setMonthlyChart(){
    var ctx = document.getElementById('monthlyBarChart');
        new Chart(ctx, {
        type: 'bar',
        data: {
            labels: dates,
            datasets: [{
                label: "Total Feed Amount",
                data: amount,
                backgroundColor: 'rgba(13, 202, 240, 0.2)',
                borderColor: 'rgba(13, 202, 240, 1)',
                borderWidth: 1
            }],
        },
        options: {
            responsive: true,
            max: amount,
            scales: {
                xAxes: [{
                    barPercentage: 0.6
                }],
                yAxes: [{
                    ticks:{beginAtZero:true},
                }]
            },
            title:{
                display: true,
                text:"Monthly Feed Totals",
                fontSize:20,
            }
        }
    })
}


































































// var current = new Date()

// var first = new Date(current.setDate(current.getDate() - current.getDay() + (current.getDay() == 0 ? -6:1)))
// var last = new Date(current.setDate(current.getDate() - current.getDay() + 7));

// Date.prototype.GetFirstDayOfWeek = function() {
//     return (new Date(this.setDate(this.getDate() - this.getDay()+ (this.getDay() == 0 ? -6:1) )));
// }
// Date.prototype.GetLastDayOfWeek = function() {
//     return (new Date(this.setDate(this.getDate() - this.getDay() +7)));
// }


// // CHART CONFIGURATION

// // CHART VARIABLES
// var endpoint = '/feedlog/chart/'

// var today = new Date();



// var dd = String(today.getDate()).padStart(2, '0');
// var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
// var yyyy = today.getFullYear();
// today = yyyy + '-' + mm + '-' + dd;
// console.log(today)

// var dd = String(first.getDate()).padStart(2, '0');
// var ymm = String(first.getMonth() + 1).padStart(2, '0'); //January is 0!
// var yyyy = first.getFullYear();
// first = yyyy + '-' + ymm + '-' + dd;
// console.log(first)
// console.log(ymm)
// console.log(last)


// $.ajax({
//     method: 'GET',
//     url: endpoint,
//     dataType: "json",
//     success: function(jsonResponse){
//         dates = jsonResponse.labels
//         amount = jsonResponse.data
        
        
//         current = dates.indexOf(today)
//         month = dates.filter(item => item.includes(ymm))
//         console.log(month)
//         // THIS DOESNT WORK COMPLETELY YET.  IT WILL FINDS DAYS THAT MATCH TOO!!!!

//         labels = dates[current]
//         data = amount[current]
//         setChart()
//     },
//     error: function(error_data){
//         console.log("error")
//         console.log(error_data)
//     }
// })

// var ctx = document.getElementById('myBarChart');
// function setChart(){
//         new Chart(ctx, {
//             type: 'bar',
//             data: {
//                 labels: [labels],
//                 datasets: [{
//                     label: "Total Feed Amount",
//                     data: [data],
//                     backgroundColor: 'rgba(13, 202, 240, 0.2)',
//                     borderColor: 'rgba(13, 202, 240, 1)',
//                     borderWidth: 1
//                 }],
//             },
//             options: {
//                 responsive: true,
//                 scales: {
//                     yAxes: [{
//                         ticks:{beginAtZero:true},
//                     }]
//                 },
//                 title:{
//                     display: false,
//                     text:"Daily Feed Amount",
//                     fontSize:20,
//                 }
//             }
//         })
// }
