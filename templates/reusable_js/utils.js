var months = new Array(12);
months[0] = "January";
months[1] = "February";
months[2] = "March";
months[3] = "April";
months[4] = "May";
months[5] = "June";
months[6] = "July";
months[7] = "August";
months[8] = "September";
months[9] = "October";
months[10] = "November";
months[11] = "December";

Number.prototype.ordinate = function(){
    var num = this,
        ones = num % 10, //gets the last digit
        tens = num % 100, //gets the last two digits
        ord = ["st","nd","rd"][ tens > 10 && tens < 20 ? null : ones-1 ] || 'th';
    return num.toString() + ord;
};

function ajaxCall(url, type, async, cache){
	var data;
	$.ajax({
		async: async, 
		cache: cache, 
		url: url,
		dataType: type,
		dataFilter: function(data) {
			var response; 
			if (type === 'json')
              return JSON.stringify(JSON.parse(data));
			else
			 return response = data;
		},
		success: function(response){
			data = response;
		}
	});
	return data;
}

function getOfficeDetails(office){
	var office_details = ajaxCall('01-DARPA-'+ office + '.json', 'json', false, true);
	return office_details;
}

function getPrograms() {
	var programs  = ajaxCall('active_content.json', 'json', false, true);
	return programs;
}

function getProgramDetails(filename) {
	var program_details = ajaxCall(filename, 'json', false, true);
	return program_details;
}

function getLicenses() {
	var licenses = ajaxCall('license-content.json', 'json', false, true);
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
		if(a[property] instanceof Date){
			if (a[property] < b[property])
				sortStatus = -1;
			else if (a[property] > b[property])
				sortStatus = 1;
		}
		else{
			if (a[property].toLowerCase().trim() < b[property].toLowerCase().trim())
				sortStatus = -1;
			else if (a[property].toLowerCase().trim() > b[property].toLowerCase().trim())
				sortStatus = 1;
		}
 
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
	var build_date = ajaxCall('last-build-date.txt', 'text', false, true);
	return build_date;
}

function getBuildDate(){
	var build_date = ajaxCall('build-date.txt', 'text', false, true);
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
    console.log(date, separator);
	var date_month = "",
	date_day = "",
	date_year = "",
	string_date = "";
	
	if(separator == "ordinal"){
		date_month = date.getMonth();
		date_day = date.getDate();
		
		string_date = months[date_month] + ' ' + date_day.ordinate();
	}
	else{
		date_month = (date.getMonth() + 1).toString().length == 1? "0" + (date.getMonth() + 1).toString() : date.getMonth() + 1;
		date_day = (date.getDate()).toString().length == 1? "0" + (date.getDate()).toString() : date.getDate();
		date_year = date.getFullYear();
		
		string_date = date_month + separator + date_day + separator + date_year;
	}
	
	
	return string_date;
}