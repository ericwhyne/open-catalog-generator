
function getPrograms() {
	var programs;
	$.ajax({
		async: false,
		url: 'active_content.json',
		dataType: 'json',
		success: function(response){
		   programs = response;
		}
	});
	
	return programs;
}

function getProgramDetails(filename) {
	var data;
	$.ajax({
		async: false,
		url: filename,
		dataType: 'json',
		success: function(response){
		   data = response;
		}
	});
	return data;
}

function isInArray(value, array) {
  //checks to see if a value exists in an array
  return array.indexOf(value) > -1;
}

function isIE() {
	var ua = window.navigator.userAgent;
	var msie = ua.indexOf("MSIE ");
	//if IE browser, return true. If another browser, return false
	if (msie > 0)      
		return true;
	else    
		return false;
}

function sortByProperty(property) {
	//sorts json array by a given property name
    return function (a, b) {
        var sortStatus = 0;
        if (a[property] < b[property])
            sortStatus = -1;
        else if (a[property] > b[property])
            sortStatus = 1;
 
        return sortStatus;
    };
}