var chart;

var utils = {};
//Could create a utility function to do this
utils.inArray = function(searchFor, property) {
 	var retVal = -1;
 	var self = this;
 	for(var index=0; index < self.length; index++){
    	var item = self[index];
     	if (item.hasOwnProperty(property)) {
        	if (item[property].toLowerCase() === searchFor.toLowerCase()) {
				retVal = index;
             	return retVal;
         	}
     	}
 	};
 	return retVal;
};

//or we could create a function on the Array prototype indirectly
Array.prototype.inArray = utils.inArray;

utils.findNode = function(series_index,nid) {
	node_id = -1
	$.each(chart.series[series_index].data, function(i, node) {
		node_id = i;
		return (node.nid != nid) ;
	});
	return node_id;
};

utils.drawNodeLinks = function() {
	// link followers to leaders
	$('.nodeLink').remove();
    var series_index = chart.series.inArray('Node', "name")
    $.each(chart.series[series_index].data, function(i, node) {
    	if(node.lid !== undefined && node.lid != 0) {
    		leader_id = utils.findNode(series_index, node.lid)
    		leader = chart.series[series_index].data[leader_id]
    		chart.renderer.path(['M',leader.plotX + chart.plotLeft, leader.plotY + chart.plotTop,
    		                     'L',node.plotX + chart.plotLeft, node.plotY + chart.plotTop]).attr({
    		                    	 'stroke-width': 1,
    		                    	 stroke: 'black',
    		                    	 dashstyle: 'dot',
    		                    	 class: 'nodeLink'
    		                    }).add();
    	}
    });	
}

/**
 * Request data from the server, add it to the graph and set a timeout 
 * to request again
 */
function requestData() {
    $.ajax({
        url: 'data/all',
        success: function(response) {

            // add the point
            $.each(response.data, function(i, r_series) {
            	var series_index = chart.series.inArray(r_series.name, "name")
            	// series hasn't been created yet, create it now
            	if(series_index = -1) {
            		chart.addSeries(r_series);
            	}
            	//chart.series[0].addPoint(value, false);	
            });                        

            chart.redraw();
            
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
            	load: requestData,
                redraw: utils.drawNodeLinks,
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
                    headerFormat: '<b>{point.key}</b><br>',
                    pointFormat: 'Location - ({point.x}, {point.y})'
                }
            },
        	series: {
        		shadow: true
        	}
        },
        series: []
    });
    renderer = new Highcharts.Renderer(
        $('#chart')[0],
        1000,
        400
    );
});