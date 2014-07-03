
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

function getLicenses() {
	var licenses;
	$.ajax({
		async: false,
		url: 'license-content.json',
		dataType: 'json',
		success: function(response){
		   licenses = response;
		}
	});
	
	return licenses;
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
        if (a[property].toLowerCase().trim() < b[property].toLowerCase().trim())
            sortStatus = -1;
        else if (a[property].toLowerCase().trim() > b[property].toLowerCase().trim())
            sortStatus = 1;
 
        return sortStatus;
    };
}

function sortByMultipleProperties(property1, property2) {

	var property_a = property_b = property1;
    return function (a, b) {

        var sortStatus = 0;
		
		if(typeof(a[property_a]) == "undefined")
			property_a = property2;
		if(typeof(b[property_b]) == "undefined")
			property_b = property2;
		
        if (a[property_a].toLowerCase().trim() < b[property_b].toLowerCase().trim())
            sortStatus = -1;
        else if (a[property_a].toLowerCase().trim() > b[property_b].toLowerCase().trim())
            sortStatus = 1;
 
		property_a = property_b = property1;
        return sortStatus;
    };
}

function getStringArray(object) {
	return object = typeof object == 'string' ? [object] : object;
}

function toCamelCase(str) {
	return str.replace(/(?:^|\s)\w/g, function(match) {
	  return match.toUpperCase();
	});
}