#!/usr/bin/python

def timeline_head():
  return """
  <!DOCTYPE html>
  <html lang='en'>
  <head>
  <meta charset="utf-8">
  <link href="css/nv.d3.css" rel="stylesheet" type="text/css">
  <link href="css/banner_style.css" rel="stylesheet" type="text/css">
  <link rel="stylesheet" type="text/css" href="css/header_footer.css"/>  
  <link rel='stylesheet' href='css/flick/jquery-ui-1.10.4.custom.css' type='text/css'/>
  <script type='text/javascript' src="d3.v3.js"></script>
  <script type='text/javascript' src="nv.d3.js"></script>
  <script type='text/javascript' src="tooltip.js"></script>
  <script type='text/javascript' src="nv.utils.js"></script>
  <script type='text/javascript' src="utils.js"></script>
  <script type='text/javascript' src="legend.js"></script>
  <script type='text/javascript' src="axis.js"></script>
  <script type='text/javascript' src="distribution.js"></script>
  <script type='text/javascript' src="scatter.js"></script>
  <script type='text/javascript'  src="scatterChart.js"></script>
  <script type='text/javascript' src='jquery-latest.js'></script>

  </head>
  <style>

  body {
    overflow: hidden;
    margin: 0;
    padding: 0;
    background-color: #C0C0C0 /*#868686*/; 
  }
  
  #timeline {
    border: 0;
    margin: 0;
  }
  
  </style>
    
  <body>
"""

def timeline_html():
  html = "<header class='darpa-header'><div class='darpa-header-images'><a href='http://www.darpa.mil/'><img class='darpa-logo' src='darpa-transparent-v2.png'></a><a href='index.html' class='programlink'><img src='Open-Catalog-Single-Big.png'></a></div>"
  html += "<div class='darpa-header-text no-space'><span><font color='white'> / </font><a href=\"change_timeline.html\"' class='programlink visheader'>Change Timeline</a></span></div></header>"

  html += """
    <br>
    <div id="offsetDiv">
      <div id="timeline" class='with-3d-shadow with-transitions'>
        <svg></svg>
      </div>
    </div>
  """
  return html
  
def timeline_script(): 
  return """
  
  <script type='text/javascript'>
  var window_height = $(window).height();
  var window_width = $(window).width();
  var date_start = new Date();
  date_start.setDate(date_start.getDate() - 31);
  var date_end = new Date();
  var min = 1;
  var max = 30;
  var offices = [{"name":"AEO", "color":"#B71500"}, {"name":"BTO", "color":"#D35C00"}, {"name":"DSO", "color":"#EBAF00"}, {"name":"I2O", "color":"#4C9509"}, {"name":"MTO", "color":"#31B7D7"}, {"name":"STO", "color":"#4682B4"}, {"name":"TTO", "color":"#55399A"}];


  $( document ).ready(function() {
  
    var programs = getPrograms();
    var data_store = createDataStore(programs);
	createTimeline(data_store);
	
  	window.onresize = function () {
		window_height = $(window).height();
		window_width = $(window).width();
		$('#chart').height(window_height - 220);
	};
  });
 
 
  function createTimeline(store){
	  var chart;
	  var chars = ""; 
	  var char_array = [];

	  for(i=65; i<=90; i++){
		 chars += String.fromCharCode(i);
		 char_array[i - 65] = String.fromCharCode(i);
	  }	 

	  //console.log(nv);
	  nv.addGraph(function() {
		chart = nv.models.scatterChart()
			.showDistX(true) //show ticks on x-axis
			.showDistY(true) //show ticks on y-axis
			.size(1).sizeRange([130,130]) //size of plot points all the same
			.transitionDuration(300);
		
		var margin = {top: 30, right: 20, bottom: 30, left: 40},
		width = 960 - margin.left - margin.right,
		height = 500 - margin.top - margin.bottom;
		
		var x = d3.scale.ordinal()
		.domain(chars.split(""))
		.rangePoints([0, width]);

		var y = d3.scale.linear()
		.range([height, 0]);

		chart.xAxis.tickSize(5).scale(x)
			.ticks(4)
			.orient("bottom")
			.rotateLabels(-30) 			
			.tickFormat(function(d) {
				var date = new Date(d);
				return d3.time.format('%m-%d-%Y')(date);
			});

		chart.yAxis.tickSize(5).scale(y)
			.ticks(10)
			.orient("left")    
			.tickFormat(function(d,i){ /*console.log(d);*/ return d; });
				
		chart.scatter.onlyCircles(false); //We want to show shapes other than circles.
	  
		chart.tooltipContent(function(office, date, total, values) {
			var p = document.createElement("p");
			p.id = "tooltip-content";
			p.setAttribute("class", "ribbon-dialog-text");
			var html = values.point.date_type + " : " + values.point.string_date;
			
			if (values.point.sw_count)
				html += "<br>Software Count : "  + values.point.sw_count;
			if (values.point.pb_count)
				html += "<br>Publications Count : "  + values.point.pb_count;						
			p.innerHTML = html;
			
			var title_div = document.createElement("div");
			title_div.id = "tooltip-title";

			if(values.point.date_type.toLowerCase() == "updated")
				title_div.setAttribute("class", "vertical-green ribbon-dialog");
			if(values.point.date_type.toLowerCase() == "new")
				title_div.setAttribute("class", "vertical-red ribbon-dialog");
			
			if (values.point.sw_count || values.point.pb_count)	
				title_div.innerHTML = values.point.program + " Entries";
			else
				title_div.innerHTML = values.point.program + " Program";

			var div = document.createElement("div");
			div.id = "tooltip";
			
			div.appendChild(title_div);
			div.appendChild(p);
			return div.outerHTML;
		});

		d3.select('#timeline svg')
			.datum(fetchData(store))
			.attr("id", "chart")
			.attr("height", window_height - 220)
			.style("margin-left", "-10")
			.call(chart);

		nv.utils.windowResize(chart.update);
		chart.dispatch.on('stateChange', function(e) { ('New State:', JSON.stringify(e)); });
		return chart;
	  });
  }

  function randomDate(start, end) {
    return new Date(start.getTime() + Math.random() * (end.getTime() - start.getTime()));
  }

  function fetchData(store) { //# groups,# points per group
    var data = [], random = d3.random.normal();
	
    //builds group array in this case, offices
	for (i = 0; i < offices.length; i++) {
      data.push({
        key: offices[i].name,
        values: [],
	    color: offices[i].color
      });
  
	  if(store["office"][3] == offices[i].name){ //check to see which office is I2O
		  var office_data = store["office"]["I2O"];
		// console.log(office_data);
		  for (j = 0; j < office_data.length; j++) {
				if(office_data[j].entries){
					var entries = office_data[j].entries;
					for(entry in entries){
						var date = stringToDate(entries[entry].Date);
						var sw_count = pb_count = 0;
						if (entries[entry]["Software"])
							sw_count = entries[entry]["Software"].length;
						if (entries[entry]["Publications"])
							pb_count = entries[entry]["Publications"].length;	
						var total_count = sw_count + pb_count;
	
						data[i].values.push({
						  y: total_count, 
						  x: date,
						  color: offices[i].color,
						  shape: "circle",
						  program: office_data[j].program,
						  date_type: entries[entry]["Date Type"],
						  string_date: dateToString(date, "-"),
						  sw_count: sw_count,
						  pb_count: pb_count
						});
					}
				}
				else{
					var date = stringToDate(office_data[j].Date);
					
					data[i].values.push({
					  y: 1, 
					  x: date,
					  color: offices[i].color,
					  shape: "circle",
					  program: office_data[j].program,
					  date_type: office_data[j]["Date Type"],
					  string_date: dateToString(date, "-")
					});
				}
		  }
	  }  
    }
    return data;
  }
  
  function createDataStore(programs){
  		var node = new Array();
		var root = new Array();
		
		for (program in programs){
		  var program_nm = programs[program]["Program Name"];
		  var dates = new Array();
		  var sw = new Array();
		  var pub = new Array();
		  var edge = new Array();
		  
		 if(programs[program]["Banner"] != ""){
			var last_build_date = stringToDate(getLastBuildDate());
			node.push({"program":program_nm, "Date": last_build_date, "Date Type": programs[program]["Banner"]});
		  }
		  		  
		  if(programs[program]["Software File"] != ""){
			  var program_sw_file = getProgramDetails(programs[program]["Software File"]);
			  for (sw_item in program_sw_file){
				var sw_object = program_sw_file[sw_item];
				var modification = getModificationDate(sw_object["New Date"], sw_object["Update Date"]);
				var mod_date = stringToDate(modification["Date"]);
				if(modification["Date"] && (mod_date >= date_start && mod_date <= date_end)){
					if(edge.length < 1)
						edge.push({"Software" : [sw_object["Software"]], "Date Type" : modification["Date Type"], "Date" : modification["Date"]});
					else{
						for (entry in edge){
							var curr_entry = edge[entry];
							if(curr_entry["Date"] == modification["Date"] && curr_entry["Date Type"] == modification["Date Type"]){
								
								if(curr_entry["Software"])
									curr_entry["Software"].push(sw_object["Software"]);
								else
									curr_entry["Software"] = [sw_object["Software"]];
								
								break;
							}
							if(entry == edge.length - 1)
								edge.push({"Software" : [sw_object["Software"]], "Date Type" : modification["Date Type"], "Date" : modification["Date"]});
						}
						
					}
				}
			  }
		  }
  		
		  if(programs[program]["Pubs File"] != ""){
			  var program_pub_file = getProgramDetails(programs[program]["Pubs File"]);
			  
			  for (pub_item in program_pub_file){
				var pub_object = program_pub_file[pub_item];
				var modification = getModificationDate(pub_object["New Date"], pub_object["Update Date"]);
				var mod_date = stringToDate(modification["Date"]);
				if(modification["Date"] && mod_date >= date_start && mod_date <= date_end){
					if(edge.length < 1){
						edge.push({"Publications" : [pub_object["Title"]], "Date Type" : modification["Date Type"], "Date" : modification["Date"]});
					}
					else{
						for (entry in edge){
							var curr_entry = edge[entry];
							if(curr_entry["Date"] == modification["Date"] && curr_entry["Date Type"] == modification["Date Type"]){
								if(curr_entry["Publications"])
									curr_entry["Publications"].push(pub_object["Title"]);
								else
									curr_entry["Publications"] = [pub_object["Title"]];
									
								break;
							}
							if(entry == edge.length - 1)
								edge.push({"Publications" : [pub_object["Title"]], "Date Type" : modification["Date Type"], "Date" : modification["Date"]});
						}
					}
				}
			  }
		  }
		  
		  if(edge.length != 0)
			node.push({"program":program_nm, "entries": edge});
		}
		
		//console.log(node);
		root = {"office":["AEO", "BTO", "DSO", "I2O", "MTO", "STO", "TTO"]};
		root["office"]["I2O"] = node;
		return root;
  }
  
  </script>
"""