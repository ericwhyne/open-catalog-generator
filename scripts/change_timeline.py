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
  <script src="d3.v3.js"></script>
  <script src="nv.d3.js"></script>
  <script src="tooltip.js"></script>
  <script src="nv.utils.js"></script>
  <script src="utils.js"></script>
  <script src="legend.js"></script>
  <script src="axis.js"></script>
  <script src="distribution.js"></script>
  <script src="scatter.js"></script>
  <script src="scatterChart.js"></script>
  <script type='text/javascript' src='jquery-latest.js'></script>

  </head>
  <style>

  body {
    overflow-y:scroll;
    margin: 0;
    padding: 0;
    background-color: #C0C0C0 /*#868686*/; 
  }

  div {
    border: 0;
    margin: 0;
  }
  
  #timeline {
    margin: 0;
  }
  
  #timeline svg {
    height: 520px;
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
  var active_programs = new Array();
  var window_height = $(window).height();
  var window_width = $(window).width();

  
  $( document ).ready(function() {
  
    var programs = getPrograms();
    var data_store = createDataStore();
  
  	window.onresize = function () {
		window_height = $(window).height();
		window_width = $(window).width();
		/*$('#vis_view').empty();
		$('#vis_view').html(getProgramView());
		$("#sunburst").empty();
		createSunburstGraph('#sunburst');*/
	};
  });
 
  var chart;
  var date_start = new Date();
  date_start.setDate(date_start.getDate() - 31);
  var date_end = new Date();
  var offices = [{"name":"AEO", "color":"#B71500"}, {"name":"BTO", "color":"#D35C00"}, {"name":"DSO", "color":"#EBAF00"}, {"name":"I2O", "color":"#4C9509"}, {"name":"MTO", "color":"#31B7D7"}, {"name":"STO", "color":"#4682B4"}, {"name":"TTO", "color":"#55399A"}];

  var chars = ""; 
  var char_array = [];
  var min = 1;
  var max = 30;

  for(i=65; i<=90; i++){
     chars += String.fromCharCode(i);
	 char_array[i - 65] = String.fromCharCode(i);
  }	 
	 
  //console.log(chars);
  //console.log(nv);
  nv.addGraph(function() {
	chart = nv.models.scatterChart()
		.showDistX(true) //show ticks on x-axis
		.showDistY(true) //show ticks on y-axis
		.size(1).sizeRange([130,130]) //size of plot points all the same
		.transitionDuration(300);

	//console.log(chart);
		
	var margin = {top: 30, right: 20, bottom: 30, left: 40},
	//width = 960 - margin.left - margin.right,
	//height = 500 - margin.top - margin.bottom;
	
	
	/*var graph_top = graph_bottom = graph_left = graph_right = 0;
	
	//calculate the graph margins and radius
	graph_top = graph_bottom = window_height * .40222;
	graph_right = graph_left = window_width * .26042;
	margin = {top: graph_top, right: graph_right, bottom: graph_bottom, left: graph_left}; //bottom and top resizes graph*/
	
	width = 960 - margin.left - margin.right,
	height = 580 - margin.top - margin.bottom;
	
	var x = d3.scale.ordinal()
    .domain(chars.split(""))
    .rangePoints([0, width]);

	var y = d3.scale.linear()
	.range([height, 0]);

	chart.yAxis.tickSize(5).scale(y)
		.ticks(10)
		.orient("left")         
		.tickFormat(function(d) {
			var date = new Date(d);
			return d3.time.format('%m-%d-%Y')(date);
		});

	chart.yAxis.tickValues(d3.time.day.range(
				date_start,
				date_end)
			);
			
	chart.xAxis.tickSize(5).scale(x)
		.ticks(4)
		.orient("bottom")
		//.rotateLabels(-30)           
		//.tickValues(d3.range(30));
		//.tickFormat(function(d,i){ return char_array[i]; })
		//.tickValues(d3.range(30));
		.tickFormat(function(d,i){ /*console.log(d);*/ return d; })
		.tickValues([1, 5, 10, 15, 20, 25, 30]);
			
    //We want to show shapes other than circles.
    chart.scatter.onlyCircles(false);
  
	chart.tooltipContent(function(key) {
	
		var p = document.createElement("p");
		p.id = "tooltip-content";
		p.setAttribute("class", "ribbon-dialog-text");
		p.innerHTML = "hello all<br>good times";
		//console.log(p);
		
		var title_div = document.createElement("div");
		title_div.id = "tooltip-title";
		title_div.setAttribute("class", "vertical-green ribbon-dialog");
		title_div.innerHTML = key + " Office";
		
		//console.log(title_div);
		
		var div = document.createElement("div");
		div.id = "tooltip";
		
		div.appendChild(title_div);
		div.appendChild(p);
		//console.log(div);
		
		return div.outerHTML;
		
		//return '<div id="tooltip"><div id="tooltip-title" class="vertical-green ribbon-dialog">' + key + ' Office</div><p id="tooltip-content" class="ribbon-dialog-text">hello all<br>good times</p></div>';
	});

	d3.select('#timeline svg')
		.datum(fetchData(4,10, x))
		.call(chart);
		
	/*console.log(d3.select('#timeline svg').selectAll("g"));
	console.log(d3.select('#timeline svg').select('.nv-legendWrap'));*/
	
	d3.select('#timeline svg').select('.nv-legendWrap')
		.attr("transform","translate(20,-38)")
		.style("font-size","12px");

	//console.log(d3.select('#timeline svg').select('.nv-point-paths'));
	
	nv.utils.windowResize(chart.update);

	chart.dispatch.on('stateChange', function(e) { ('New State:', JSON.stringify(e)); });

	return chart;
  });
  
  

  function randomDate(start, end) {
    return new Date(start.getTime() + Math.random() * (end.getTime() - start.getTime()));
  }

  function fetchData(groups, points, x) { //# groups,# points per group
    var data = [],
      random = d3.random.normal();
    //builds group array in my case, offices
    for (i = 0; i < offices.length; i++) {
      data.push({
        key: offices[i].name,
        values: [],
	    color: offices[i].color
      });
  
      for (j = 0; j < points; j++) {
        data[i].values.push({
          y: randomDate(date_start, date_end), 
          x: Math.floor(Math.random() * (max - min + 1) + min), //needs to 
		  color: offices[i].color,
          shape: "circle"
        });
      }
    }
    return data;
  }
  
  function createDataStore(){
  		var node = new Array();
		var root = new Array();
		
		for (program in programs){
		  var program_nm = programs[program]["Program Name"];
		  var dates = new Array();
		  var sw = new Array();
		  var pub = new Array();
		  var edge = new Array();
		  
		  if(programs[program]["Software File"] != ""){
			  var program_sw_file = getProgramDetails(programs[program]["Software File"]);
			  for (sw_item in program_sw_file){
				var sw_object = program_sw_file[sw_item];
				var modification = getModificationDate(sw_object["New Date"], sw_object["Update Date"]);
				
				if(modification["Date"]){
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
				
				if(modification["Date"] != ""){
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
		
		root.push({"office":"I20", "modifications": node});
		return root;
  }
  
  </script>
"""