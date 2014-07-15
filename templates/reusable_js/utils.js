
function getPrograms() {
	var programs;
	$.ajax({
		async: false, 
		cache: false, 
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
		cache: false, 
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
		cache: false, 
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
	//check for ie10 and below or ie. If IE browser, return true. If another browser, return false
	if (msie > 0 || window.navigator.msMaxTouchPoints !== void 0 )    
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

function validEmail(item) {
	
	var value = null;
	
	if(item.value) value = item.value;
	else value = item;
		
	var filter = /(([a-zA-Z0-9\-?\.?]+)@(([a-zA-Z0-9\-_]+\.)+)([a-z]{2,3}))+$/;
	return filter.test(value);
}

function getModificationDate(new_date, update_date){
	var change_date = "", change_text = "";
	var change_set = [];

	if(new_date == "" && update_date == ""){
		change_set["Date Type"] = change_text;
		change_set["Date"] = change_date;
	}
	else{
		if (new_date != "" && update_date != ""){
			if (new_date >= update_date){
			 change_date = new_date;
			 change_text = "NEW";
			}
			else{
			  change_date = update_date;
			  change_text = "UPDATED";
			}
		}
		else if( new_date != "" && update_date == ""){
			change_date = new_date;
			change_text = "NEW";
		}
		else if(update_date != "" && new_date == ""){
			change_date = update_date;
			change_text = "UPDATED";
		}
		
		change_set["Date Type"] = change_text;
		change_set["Date"] = change_date;
	}

	return change_set;
}


function getLastBuildDate(){
	var build_date;
	$.ajax({
		async: false, 
		cache: false, 
		url: 'last-build-date.txt',
		dataType: 'text',
		success: function(response){
		   build_date = response;
		}
	});
	return build_date;
}

function stringToDate(text){
	var pattern1 = /\d{4}\d{2}\d{2}/;
	var pattern2 = /\d{4}\-\d{2}\-\d{2}/;
	var dt = "";
	
	if(pattern1.exec(text))
		dt = new Date(text.substring(0,4), parseInt(text.substring(4,6)) - 1, text.substring(6,8)); // - 1 because months starts from 0.
	else if (pattern2.exec(text)){
		text = text.split("-");
		dt = new Date(text[0], parseInt(text[1]) - 1, text[2]); // - 1 because months starts from 0.
	}
	else
		dt = new Date(text);

	return dt;
}


function dateToString(date, separator){
	var date_month = (date.getMonth() + 1).toString().length == 1? "0" + (date.getMonth() + 1).toString() : date.getMonth() + 1;
	var date_day = (date.getDate()).toString().length == 1? "0" + (date.getDate()).toString() : date.getDate();
	var date_year = date.getFullYear();
	
	var string_date = date_month + separator + date_day + separator + date_year;
	return string_date;
}