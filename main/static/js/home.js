var chart;

/**
 * Request data from the server, add it to the graph and set a timeout 
 * to request again
 */
function requestData() {
    $.ajax({
        url: 'data/all',
        success: function(response) {
            var series = chart.series[0],
                shift = series.data.length > 20; // shift if the series is 
                                                 // longer than 20

            // add the point
            $.each(response.data, function(index, value) {
            	chart.series[0].addPoint(value, false);	
            });
            chart.redraw()
            
            // call it again after one second
            //setTimeout(requestData, 1000);    
        },
        cache: false
    });
}

$(function () {
	chart = new Highcharts.Chart({
        chart: {
        	renderTo: 'chart',
            type: 'scatter',
            zoomType: 'xy',
            width: 1000,
            events: {
            	load: requestData
            }
        },
        title: {
            text: 'Random Scatter'
        },
        plotOptions: {
            scatter: {
                marker: {
                    radius: 5,
                    states: {
                        hover: {
                            enabled: true,
                            lineColor: 'rgb(100,100,100)'
                        }
                    }
                },
                states: {
                    hover: {
                        marker: {
                            enabled: false
                        }
                    }
                },
                tooltip: {
                    headerFormat: '<b>Location</b><br>',
                    pointFormat: '{point.x}, {point.y}'
                }
            }
        },
        series: [{
            name: 'Random data',
            data: []
        }]
    });
});