var table = document.getElementById('weightTable');

var recorded_weight = [];
var recorded_date = [];

for (var i = 1; i < table.rows.length; i++) {
    recorded_weight.push([
        parseFloat(table.rows[i].cells[1].innerHTML)
    ]);

    recorded_date.push([
        table.rows[i].cells[0].innerHTML
    ]);
}

var values = recorded_weight.flat();

// WEIGHT LINE CHARTS - WEIGHT BY DATE

// settings to set defaults to mimic current website styling
Chart.defaults.global.defaultFontFamily = 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", "Liberation Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"';
Chart.defaults.global.defaultFontColor = '#858796';


// MONTHLY CHART.JS CONFIGURATION + LABELS & DATA
var ctx = document.getElementById('weightChart')
var weightChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [...recorded_date],
        datasets: [{
            label: "Weights",
            data: values,
            backgroundColor: 'rgba(13, 202, 240, 0.2)',
            borderColor: 'rgba(13, 202, 240, 1)',
            pointRadius: 5,
            pointBackgroundColor: 'rgba(13, 202, 240, 1)',
            pointBorderColor: 'rgba(255,255,255,0.8)',
            pointHoverRadius: 5,
            pointHoverBackgroundColor: 'rgba(13, 202, 240, 1)',
            pointHitRadius: 50,
            pointBorderWidth: 2,
        }],
    },
    options: {
        responsive: true,
        scales: {
            xAxes: [{
                ticks: {
                    autoSkip: false,
                    maxRotation: 60,
                    minRotation: 60
                },
                gridLines: {
                    display: true
                },

            }],
            yAxes: [{
                ticks: {
                    min: 0,
                    maxTicksLimit: 12,
                    padding: 10,
                    // Include a 'kg' in the ticks
                    callback: function(value, index, values) {
                        var units = document.getElementById('units').innerHTML
                        return value + units;
                    }
                },
                gridLines: {
                    color: "rgba(0, 0, 0, .125)",
                },
                scaleLabel: {
                    display: true,
                    padding: 10,
                    fontColor: '#555759',
                    fontSize: 16,
                    fontStyle: 700,
                    labelString: 'Past Weight'
                },
            }],
        },
        legend: {
            display: true,
            position: 'top',
        },
        title: {
            display: true,
            text:"Weight History",
            fontSize:20,
        }
    }
});