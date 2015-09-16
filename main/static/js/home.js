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
	$('.nodeVector').remove();
    var series_index = chart.series.inArray('Node', "name")
    $.each(chart.series[series_index].data, function(i, node) {
    	// draw line to its leader
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
    	// draw current speed and dir
    	if(node.speed !== 0.0 || node.dir != 0.0) {
    		x = node.plotX
    		y = node.plotY
    		newX = Math.cos(((node.dir-90)%360)*Math.PI/180) * (node.speed/3.0*100) + node.plotX
    		newY = Math.sin(((node.dir-90)%360)*Math.PI/180) * (node.speed/3.0*100) + node.plotY
    		chart.renderer.path(['M',node.plotX + chart.plotLeft, node.plotY + chart.plotTop,
    		                     'L',newX + chart.plotLeft, newY + chart.plotTop]).attr({
    		                    	 'stroke-width': 2,
    		                    	 stroke: 'black',
    		                    	 class: 'nodeVector'
    		                    }).add();
    	}
    	// draw current force vector
    	if(node.fspeed !== 0.0 || node.fdir != 0.0) {
    		x = node.plotX
    		y = node.plotY
    		newX = Math.cos(((node.fdir-90)%360)*Math.PI/180) * (node.fspeed/1.0*100) + node.plotX
    		newY = Math.sin(((node.fdir-90)%360)*Math.PI/180) * (node.fspeed/1.0*100) + node.plotY
    		chart.renderer.path(['M',node.plotX + chart.plotLeft, node.plotY + chart.plotTop,
    		                     'L',newX + chart.plotLeft, newY + chart.plotTop]).attr({
    		                    	 'stroke-width': 2,
    		                    	 stroke: 'yellow',
    		                    	 class: 'nodeForce'
    		                    }).add();
    	}
    });	
}

utils.addGoal= function(e) {
    var x = e.xAxis[0].value;
    var y = e.yAxis[0].value;
    var jp_series = this.series[1];
    var g_series = this.series[3];
    
	var my_data = []
	mydata = {
        'lon':  x,
       	'lat': y,
       	'leader': 0
    }
	$.ajax({
	  url: '/data/addGoal',
	  data: JSON.stringify(mydata, null, '\t'),
	  type: 'POST',
	  contentType: 'application/json;charset=UTF-8',
	  success: function(response) {
		console.log(response);
        if(response.status == 'OK') {  
    		// Add it
    		//jp_series.addPoint([x, y]);
    		g_series.addPoint([x, y]);
        } else {
        	// didn't receive correct status code from server
        	// error occured
        	alert(response.msg);
        }
	    return false;
	  },
	  error: function(error) {
	    console.log(error);
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
            width: 925,
            plotBackgroundImage: '/static/images/track.png',
            events: {
            	load: requestData,
                redraw: utils.drawNodeLinks,
				click: utils.addGoal,
            }
        },
        title: {
            text: 'Overview Map'
        },
        xAxis: {
        	labels: {enabled:false},
        	min: -79.970725,
        	max: -79.969341
        	//min:  -79.970895,
        	//max:  -79.968527
        },
        yAxis: {
        	labels: {enabled:false},
        	min: 32.995823,
        	max: 32.997072
        	//min:  32.995984,
            //max: 32.997162
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
                    pointFormat: 'Location: ({point.y}, {point.x})'
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
        925,
        1000
    );
});