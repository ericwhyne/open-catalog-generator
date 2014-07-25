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
  html += "<div class='darpa-header-text no-space'><span><font color='white'> / </font><a href=\"change_timeline.html\"' class='programlink visheader'>What's New Timeline</a></span></div></header>"

  html += """
    <br>
	<div id="feed" class="slider">
	</div>
    <div id="offsetDiv"  style="float:left; width:76%">
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
  var active_offices = [];
  var url_href = window.location.href;
  var url_path = url_href.substring(0, url_href.lastIndexOf("/"));


  $( document ).ready(function() {
  
    var programs = getPrograms();
    var data_store = createDataStore(programs);
	activateDataCarousel(data_store);
	createTimeline(data_store);
  	window.onresize = function () {
		window_height = $(window).height();
		window_width = $(window).width();
		$('.slider').height(window_height - 250);
		$('#timeline svg').height(window_height - 220);
	};
  });
 
  function activateDataCarousel(store){
	// settings
	var slider = $('.slider'); // class or id of carousel slider
	var slide = 'div';
	var transition_in_time = 1500; // 1.5 second
	var time_between_slides = 30000; // 30 seconds
	var transition_out_time = 0;
	
	var html = "";
	var prev_program = "";

	for(office in store.offices){
		var office_data = store.offices[store.offices[office]];
		for (data in office_data) {
			var type_class = "";
			if(prev_program != office_data[data].program){
				html = "<div class='slider-div' style='font-size:75%; display:none; height:98%;'>";
				html += "<p style='width:100%; display:inline-block; background-color: black; margin:0; border-bottom:solid 2px white;'>";
				html += "<span style='color: #" + office_data[data].office["DARPA Office Color"] + "; width:34%; float:left; font-size:20px; font-weight:bold; padding-left:4px;'>" + office_data[data].program + "</span>"; //get color of I2O office
				
				if(!office_data[data].projects){
					
					if(office_data[data]["Date Type"].toLowerCase() == "updated")
						type_class = "vertical-green";
					else
						type_class = "vertical-red";
				
					html += "<span style='font-size:13px; width:62%; float:right; line-height:26px; text-align:right; padding-right:4px; color:white;'><span class='" + type_class + "'>" + office_data[data]["Date Type"] + "</span> PROGRAM : " + dateToString(office_data[data]["Date"], "-") + "</span>";
				}	
				html += "</p>";
			}
			else{
					html = "";	
			}
				
			if(office_data[data].projects){
				var projects = office_data[data].projects;
				 projects.sort(sortByProperty('Date'));
				var url_redirect =  url_path + "/" + office_data[data].program + ".html";
				html += "<div class='projects-div' style='overflow-x: hidden; overflow-y: auto; height:90%; margin:0px 2px 0px 5px;'>";
				for (project in projects) {
					
					if(projects[project]["Date Type"].toLowerCase() == "updated")
						type_class = "vertical-green";
					else
						type_class = "vertical-red";
						
					html += "<p style='text-align:center; width:100%;'><span class='" + type_class + "'>" + projects[project]["Date Type"] + "</span> : " + dateToString(projects[project]["Date"], "-") + "</p>";
					
					if(projects[project]["Publications"]){
						var publications = projects[project]["Publications"];
						for(pb in publications){
							html += "<p style='width:100%;'>Publication : <a href=" + url_redirect + "?tab=tabs1&term=" + encodeURIComponent(publications[pb]) + ">" + publications[pb] + "</a></p>"; //redirect to publications search
						}
					}
					if(projects[project]["Software"]){
						var software = projects[project]["Software"];
						for(sw in software){
							html += "<p style='width:100%;'>Software : <a href=" + url_redirect + "?tab=tabs0&term=" + encodeURIComponent(software[sw]) + ">" + software[sw] + "</a></p>"; //redirect to software search
						}
					}
					html += "<hr>";
				}
				html += "</div>";
			}
			else{
				if ((typeof(office_data[parseInt(data) + 1]) == "object" && (office_data[data].program != office_data[parseInt(data) + 1].program)) || typeof(office_data[parseInt(data) + 1]) == "undefined" && !office_data[data].projects)
					html += "<p style='text-align:center; width:100%;'>No projects for this program have been updated in the past 31 days.</p>";
			}

			if(prev_program != office_data[data].program){
				html += "</div>";
				slider.append(html);
			}
			else{
				slider[0].lastChild.innerHTML = slider[0].lastChild.innerHTML + html;
			}
			prev_program = office_data[data].program; //AA
		}
	}
	  
	slider.height(window_height - 250);
	slider.css("display", "inline");
	
	function slides(){
	  return $(".slider-div"); 
	}

	slides().first().addClass('active');
	slides().first().fadeIn(transition_in_time);
	
	// auto scroll 
	interval = setInterval(
		function(){
		  var i = slider.find(slide + '.active').index();
		  slides().eq(i).fadeOut(transition_out_time);		  
		  slides().eq(i).removeClass('active');

		  if (slides().length == i + 1)
			i = -1; // loop to start from the beginning

		  slides().eq(i + 1).addClass('active');
		  slides().eq(i + 1).fadeIn(transition_in_time);
		  
		}
		, transition_in_time +  time_between_slides 
	);

  }	
  
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
		
		chart.xAxis.tickSize(3).scale(x)
			.ticks(4)
			.orient("bottom")
			.rotateLabels(-30) 			
			.tickFormat(function(d) {
				var date = new Date(d);
				return d3.time.format('%m-%d-%Y')(date);
			});

		chart.yAxis.tickSize(3).scale(y)
			.ticks(5)
			.orient("left")    
			.tickFormat(function(d,i){ /*console.log(d);*/ return d; });
				
		chart.scatter.onlyCircles(false); //We want to show shapes other than circles.
	  
		chart.tooltipContent(function(office, date, total, values) {
			var type_class = "";
			if(values.point.date_type.toLowerCase() == "updated")
				type_class = "vertical-green";
			if(values.point.date_type.toLowerCase() == "new")
				type_class = "vertical-red";
		
			var p = document.createElement("p");
			p.id = "tooltip-content";
			p.setAttribute("class", "ribbon-dialog-text");
			var html =  "<span class='" + type_class + "'>" + values.point.date_type + "</span> : " + values.point.string_date;
			
			if (values.point.sw_count)
				html += "<br>Software Count : "  + values.point.sw_count;
			if (values.point.pb_count)
				html += "<br>Publications Count : "  + values.point.pb_count;						
			p.innerHTML = html;
			
			var title_div = document.createElement("div");
			title_div.id = "tooltip-title";
			title_div.setAttribute("class", "ribbon-dialog");

			if (values.point.sw_count || values.point.pb_count)	
				title_div.innerHTML = "<span style=' color:#" + values.point.color + ";'>" + values.point.program + " Projects</span>";
			else
				title_div.innerHTML = "<span style=' color:#" + values.point.color + ";'>" + values.point.program + " Program</span>";

			title_div.style.color = values.point.color;
			var div = document.createElement("div");
			div.id = "tooltip";
			
			div.appendChild(title_div);
			div.appendChild(p);
			return div.outerHTML;
		});

		d3.select('#timeline svg')
			.datum(fetchTimelineData(store))
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

  function fetchTimelineData(store) { //# groups,# points per group
    var data = [], random = d3.random.normal();
	
    //builds group array in this case, active_offices
	for (i = 0; i < active_offices.length; i++) {
      data.push({
        key: active_offices[i].name,
        values: [],
	    color: "#" + active_offices[i].color
      });
      
	  for (j = 0; j < store.offices.length; j++) {
		    var office_data = store.offices[store.offices[j]];
			for (office in office_data) {
			  if(office_data[office].office["DARPA Office"] == active_offices[i].name){
				if(office_data[office].projects){
					//console.log(office_data[office].projects);
					var projects = office_data[office].projects;
					for(project in projects){
						var date = stringToDate(projects[project].Date);
						var sw_count = pb_count = 0;
						if (projects[project]["Software"])
							sw_count = projects[project]["Software"].length;
						if (projects[project]["Publications"])
							pb_count = projects[project]["Publications"].length;	
						var total_count = sw_count + pb_count;
	
						data[i].values.push({
						  y: total_count, 
						  x: date,
						  color: "#" + active_offices[i].color,
						  shape: "circle",
						  program: office_data[office].program,
						  date_type: projects[project]["Date Type"],
						  string_date: dateToString(date, "-"),
						  sw_count: sw_count,
						  pb_count: pb_count
						});
					}
				}
				else{
					var date = stringToDate(office_data[office].Date);
					
					data[i].values.push({
					  y: 1, 
					  x: date,
					  color: "#" + active_offices[i].color,
					  shape: "circle",
					  program: office_data[office].program,
					  date_type: office_data[office]["Date Type"],
					  string_date: dateToString(date, "-")
					});
				}
			  }

			}
	  }
    }
    return data;
  }
  
  function createDataStore(programs){
  		var node = new Array();
		var root = new Array();
		var office_checker = new Array();
		
		for (program in programs){
		  var program_nm = programs[program]["Program Name"];
		  //var program_office = programs[program]["DARPA Office"];
		  var dates = new Array();
		  var office_details = new Array();
		  var sw = new Array();
		  var pub = new Array();
		  var edge = new Array();
		  
		  if(programs[program]["DARPA Office"] != ""){
			office_details = getOfficeDetails(programs[program]["DARPA Office"]);

			if(!isInArray(office_details["DARPA Office"] , office_checker)){
				active_offices.push({"name":office_details["DARPA Office"], "color":office_details["DARPA Office Color"]});
				office_checker.push(office_details["DARPA Office"]);
			}
		  }
		  
		 if(programs[program]["Banner"] != ""){
			var build_date = stringToDate(getBuildDate());
			//console.log(office_details);
			//if (office_details["DARPA Office"] == "DSO")
				//build_date = new Date("July 25, 2014 11:13:00");
			node.push({"office":office_details, "program":program_nm, "Date": build_date, "Date Type": programs[program]["Banner"]});
		  }
		  	  
		  if(programs[program]["Software File"] != ""){
			  var program_sw_file = getProgramDetails(programs[program]["Software File"]);
			  for (sw_item in program_sw_file){
				var sw_object = program_sw_file[sw_item];
				var modification = getModificationDate(sw_object["New Date"], sw_object["Update Date"]);
				var mod_date = stringToDate(modification["Date"]);
				if(modification["Date"] && (mod_date >= date_start && mod_date <= date_end)){
					if(edge.length < 1)
						edge.push({"Software" : [sw_object["Software"]], "Date Type" : modification["Date Type"], "Date" : mod_date});
					else{
						for (project in edge){
							var curr_entry = edge[project];
							if(curr_entry["Date"].getTime() == mod_date.getTime() && curr_entry["Date Type"] == modification["Date Type"]){
								if(curr_entry["Software"])
									curr_entry["Software"].push(sw_object["Software"]);
								else
									curr_entry["Software"] = [sw_object["Software"]];
								
								break;
							}
							if(project == edge.length - 1)
								edge.push({"Software" : [sw_object["Software"]], "Date Type" : modification["Date Type"], "Date" : mod_date});
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
						edge.push({"Publications" : [pub_object["Title"]], "Date Type" : modification["Date Type"], "Date" : mod_date});
					}
					else{
						for (project in edge){
							var curr_entry = edge[project];
							if(curr_entry["Date"].getTime() == mod_date.getTime() && curr_entry["Date Type"] == modification["Date Type"]){
								if(curr_entry["Publications"])
									curr_entry["Publications"].push(pub_object["Title"]);
								else
									curr_entry["Publications"] = [pub_object["Title"]];
									
								break;
							}
							if(project == edge.length - 1)
								edge.push({"Publications" : [pub_object["Title"]], "Date Type" : modification["Date Type"], "Date" : mod_date});
						}
					}
				}
			  }
		  }
		  
		  if(edge.length != 0)
			node.push({"office":office_details, "program":program_nm, "projects": edge});
		}
		
		//console.log(node);
		root = {"offices": office_checker}; //offices

		for (n in node){
			for (r_office in root.offices){
				//console.log(root.offices[root.office[r_office]]);
				var curr_office = node[n].office["DARPA Office"];
				if(curr_office == root.offices[r_office]){
					if (typeof(root.offices[curr_office]) == "undefined")
						root.offices[curr_office] = [node[n]];
					else
						root.offices[curr_office].push(node[n]);
					break;
				}
					
			}
			
		}
		//console.log(root);
		return root;
  }
    
  </script>
"""