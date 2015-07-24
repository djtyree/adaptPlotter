$(function () {
    setNavigation(); 
    setConfirmDelete();
});

function setNavigation() {
    var path = window.location.pathname;
    path = path.replace(/\/$/, "");
    path = decodeURIComponent(path);

    $(".nav a").each(function () {
        var href = $(this).attr('href');
        if ((href==='/' && path==='') || ((href.length > 1) && (path.substring(0, href.length) === href))) {
            $(this).closest('li').addClass('active');
        }
    });
}

function setConfirmDelete() {
	var data_type = $('.data-table').attr('id');
	$('.btn-delete').each(function() {
		$("#"+this.id).confirmOn('click', function(e, confirmed) {
	    	if(confirmed) { // Clicked yes
	    		deleteData(data_type, this.id.substring(data_type.length + 8), this.id);	    	
	      	} else { // Clicked no
	      	}
		});
	});
}

function deleteData(type, id, domId) {
	var my_data = []
	mydata = {
        'data_id':  id,
       	'data_type': type
    }
	$.ajax({
	  url: '/data/delete',
	  data: JSON.stringify(mydata, null, '\t'),
	  type: 'POST',
	  contentType: 'application/json;charset=UTF-8',
	  success: function(response) {
		console.log(response);
        if(response.status == 'OK') {  
	      var tr = $("#"+domId).closest('tr');
	      tr.css("background-color","#FF3700");
	      tr.fadeOut(400, function(){
	        tr.remove();	   
	        var rowCount = $('.data-table tbody tr').length;
	      	if(rowCount == 0) {
		      	cols = countColumns('.data-table')
		      	var row =  $('<tr><td colspan=' + cols + '>All elements deleted. Click new to create more.</td></tr>');
		      	row.hide();
	      		$('.data-table > tbody:last-child').append(row);
	      		row.fadeIn(800);
	      	}     
	      });
	      
        } else {
        	// didn't receive correct status code from server
        	// error occured
        }
	    return false;
	  },
	  error: function(error) {
	    console.log(error);
	  }
	});
}

function countColumns(tableSelector) {
    return $(tableSelector + ' thead th').length;
}