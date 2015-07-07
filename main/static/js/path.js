function updatePositions(event, ui) {
	var $lis = $(this).children('tr:not(.template)');
    $lis.each(function() {
        var $li = $(this);
        var newVal = $(this).index() - 1;
        $(this).children('.position').val(newVal);
    });
}

function updateAfterRemove() {
	var $lis = $('.repeat table tbody').children('tr:not(.template)');
    $lis.each(function() {
        var $li = $(this);
        var newVal = $(this).index() - 1;
        $(this).children('.position').val(newVal);
    });
}

function updateAfterAdd(container, new_row) {
	var row_count = $(container).attr('data-rf-row-count');
	row_count++;
	$('*', new_row).each(function() {
		$.each(this.attributes, function(index, element) {
			this.value = this.value.replace(/{{row-count-placeholder}}/, row_count - 1);
		});
	});
	$(container).attr('data-rf-row-count', row_count);
	
	updateAfterRemove();
}


$(function () {
	$('.repeat').each(function() {
        $(this).repeatable_fields({
        	after_remove: updateAfterRemove,
        	after_add: updateAfterAdd,
        	sortable_options: { 
        		update: updatePositions,
        	}
        });
    });
});