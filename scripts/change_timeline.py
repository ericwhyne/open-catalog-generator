#!/usr/bin/python

def timeline_head():
  head = """
  <!DOCTYPE html>
  <html lang='en'>
  <head>
  <meta charset="utf-8">
  <link href="css/nv.d3.css" rel="stylesheet" type="text/css">
  <link href="css/banner_style.css" rel="stylesheet" type="text/css">
  <link rel="stylesheet" type="text/css" href="css/header_footer.css"/>  
  <link rel='stylesheet' href='css/flick/jquery-ui-1.10.4.custom.css' type='text/css'/>
  <link rel='stylesheet' href='css/style_v2.css' type='text/css'/>
  <script type='text/javascript' src="d3.v3.js"></script>
  <script type='text/javascript' src="nv.d3.js"></script>
  <script type='text/javascript' src="tooltip.js"></script>
  <script type='text/javascript' src="nv.utils.js"></script>
  <script type='text/javascript' src="utils.js"></script>
  <script type='text/javascript' src="legend.js"></script>
  <script type='text/javascript' src="axis.js"></script>
  <script type='text/javascript' src="distribution.js"></script>
  <script type='text/javascript' src='jquery-latest.js'></script>

  </head>
  <style>

  body {
    overflow: hidden;
    margin: 0;
    padding: 0;
    background-color: #C0C0C0 /*#868686*/; 
  }

  </style>
    
  <body>
  """
  
  head += "<header class='darpa-header'><div class='darpa-header-images'><a href='http://www.darpa.mil/'><img class='darpa-logo' src='darpa-transparent-v2.png'></a><a href='index.html' class='programlink'><img src='Open-Catalog-Single-Big.png'></a></div>"
  head += "<div class='darpa-header-text no-space'><span><font color='white'> / </font><a href=\"change_timeline.html\"' class='programlink visheader'>What's New Timeline</a></span></div></header>"
  
  return head
  
def timeline_html():
  html = """
	<div id="feed">
		<div id="controller">
			<input type="button" id="back" class="slide_buttons" value="<<" onclick="controlAction(this);" />
			<input type="button" id="scroll" class="slide_buttons" value="||" onclick="controlAction(this);" />
			<input type="button" id="forward" class="slide_buttons" value=">>" onclick="controlAction(this);" />
		</div>
		<div id="slide_view" class="slider">
		</div>
	</div>
    <div id="offset_div">
      <div id="timeline" class='with-3d-shadow with-transitions'>
        <svg></svg>
      </div>
    </div>
  """
  return html
  
def timeline_script(): 
  return """
  
  <script type='text/javascript'>
  var active_offices = [];
  var window_height = $(window).height(),
	window_width = $(window).width(),
	minus_feed = 440,
	minus_timeline = 380;
	
  var change_dates = new Array(),
	date_start = new Date(),
	date_end = new Date();
	date_start.setDate(date_start.getDate() - 31);
	
  var min = 1,
	max = 30;
	
  var url_href = window.location.href,
	url_path = url_href.substring(0, url_href.lastIndexOf("/"));
	
  var slider = null, // class or id of carousel slider
	interval = null,
	transition_in_time = 1000, // 1.0 second
	time_between_slides = 7000, // 7 seconds
	transition_out_time = 0;


  $( document ).ready(function() {
  
    var programs = getPrograms();
    var data_store = createDataStore(programs);
	activateDataCarousel(data_store);
	createTimeline(data_store);
  	window.onresize = function () {
		window_height = $(window).height();
		window_width = $(window).width();
	};
  });
 
  function activateDataCarousel(store){
	// settings
	var html = [];
	var prev_program = "";
	
	slider = $('.slider'); // class or id of carousel slider
	change_dates.sort();
	
	
	for (i = 0; i < change_dates.length; i++){
		for(office in store.offices){
			var office_data = store.offices[store.offices[office]];
			for (data in office_data) {
				var type_class = "";
				var url_redirect =  url_path + "/" + office_data[data].program + ".html";

				if(office_data[data].projects){
					var projects = office_data[data].projects;
					for (project in projects) {
						if(change_dates[i] == projects[project]["Date"].getTime()){
							if(typeof(html[i]) == "undefined"){
								html[i] = "<div class='slider_div'>";
								html[i] += "<p class='slide_header_p'>";
								html[i] += "<span class='slide_header_span' style='color:yellow;'>What's New</span>";
								html[i] += "<span class='slide_header_update'>" + dateToString(projects[project]["Date"], "-") + "</span>";
								html[i] += "</p>";
								
								html[i] += "<div class='projects_div'>";
							}
							
							html[i] += "<p style='text-align:center; width:100%;'><a href=" + url_redirect + "><span class='slide_project_span' style='color: #" + office_data[data].office["DARPA Office Color"] + ";'>" + office_data[data].program + "</span></a></p>";
							
							if(projects[project]["Date Type"].toLowerCase() == "updated")
								type_class = "vertical-green";
							else
								type_class = "vertical-red";
													
							if(projects[project]["Publications"]){
								var publications = projects[project]["Publications"].sort();
								for(pb in publications){
									html[i] += "<p><span class='" + type_class + "'>" + projects[project]["Date Type"] + "</span> Publication : <a href=" + url_redirect + "?tab=tabs1&term=" + encodeURIComponent(publications[pb]) + ">" + publications[pb] + "</a></p>"; //redirect to publications search
								}
							}
							if(projects[project]["Software"]){
								var software = projects[project]["Software"].sort();
								for(sw in software){
									html[i] += "<p><span class='" + type_class + "'>" + projects[project]["Date Type"] + "</span> Software : <a href=" + url_redirect + "?tab=tabs0&term=" + encodeURIComponent(software[sw]) + ">" + software[sw] + "</a></p>"; //redirect to software search
								}
							}
						}	
					}
					
				}
				else{
					if(change_dates[i] == office_data[data]["Date"].getTime()){
						if(typeof(html[i]) == "undefined"){
							html[i] = "<div class='slider_div'>";
							html[i] += "<p class='slide_header_p'>";
							html[i] += "<span class='slide_header_span' style='color:yellow;'>What's New</span>";
							html[i] += "<span class='slide_header_update'>" + dateToString(office_data[data]["Date"], "-") + "</span>";
							html[i] += "</p>";
							
							html[i] += "<div class='projects_div'>";
						}
						
						if(office_data[data]["Date Type"].toLowerCase() == "updated")
							type_class = "vertical-green";
						else
							type_class = "vertical-red";
							
						html[i] += "<p style='text-align:center; width:100%;'><span class='" + type_class + "'>" + office_data[data]["Date Type"] + "</span> <a href=" + url_redirect + "><span class='slide_project_span' style='color: #" + office_data[data].office["DARPA Office Color"] + ";'>" + office_data[data].program + "</span></a></p>";
					}
				}
				if(typeof(html[i]) != "undefined" && $(html[i])[0].lastChild.childNodes[$(html[i])[0].lastChild.childElementCount - 1].localName == "p"){
					html[i] += "<hr>";
				}
			}
		}
		
		if(html[i])
			html[i] += "</div></div>";
	}
	
	slider.append(html.join(""));
	slider.height(window_height - minus_feed);
	slider.css("display", "inline");
	
	slides().first().addClass('active');
	slides().first().fadeIn(transition_in_time);
	
	// auto scroll 
	interval = startInterval();
  }	
  
  function slides(){
	return $(".slider_div"); 
  }
  
  function startInterval(){
	return setInterval(
		function(){ slideControl(1);},
		transition_in_time +  time_between_slides 
	);
  }
  
  function slideControl(direction){
   
	var i = slider.find('div.active').index();
	//console.log(i, slider.find('div.active').value);
	slides().eq(i).fadeOut(transition_out_time);		  
	slides().eq(i).removeClass('active');
	
	//console.log(slides().length);
	if (slides().length == i + direction)
		i = -1; // loop to start from the beginning
		
	//console.log(i, slider.find('div.active').val());
	slides().eq(i + direction).addClass('active');
	slides().eq(i + direction).fadeIn(transition_in_time);
  }
  
  function controlAction(control){
	if(control.id == "scroll")
	{
		if(control.value == "||"){
			clearInterval(interval);
			$("#" + control.id).val(">");
		}
		else if(control.value == ">"){
			interval = startInterval();
			$("#" + control.id).val("||");
		}
	}
	else if(control.id == "back"){
		slideControl(-1);
		$("#" + control.id).attr("disabled", "disabled");
		setTimeout(function(){$("#" + control.id).removeAttr("disabled");}, 1000);
		
	}
	else
		slideControl(1);
		$("#" + control.id).attr("disabled", "disabled");
		setTimeout(function(){$("#" + control.id).removeAttr("disabled");}, 1000);
  }  
	  
  function createTimeline(store){
		var chart;
		var chars = ""; 
		var char_array = [];
		var id  = Math.floor(Math.random() * 100000);
		var root = fetchTimelineData(store);
		var nodes = [];
		var single_point = false;
		
		for(branch in root){
			for(node in root[branch].values)
				nodes.push(root[branch].values[node]);
		}
		
		if (nodes.length == 1)
			single_point = true;

	 nv.addGraph(function() {
	 
	 	var margin = {top: 40, right: 10, bottom: 60, left: 50},
		width = 960 - margin.left - margin.right,
		height = 500 - margin.top - margin.bottom;
		
		chart = nv.models.scatterChart()
			.showDistX(true) //show ticks on x-axis
			.showDistY(true) //show ticks on y-axis
			.id(id) 
			.size(1).sizeRange([130,130]) //size of plot points all the same
			.transitionDuration(300)
			.margin({top: margin.top, right: margin.right, bottom: margin.bottom, left: margin.left});

		var x = d3.scale.linear()
			.range([0, width]);

		var y = d3.scale.linear()
			.range([height, 0]);
		
		chart.xAxis.tickSize(3).scale(x)
			.ticks(4)
			.orient("bottom")
			.rotateLabels(-30)
			.domain([date_start, date_end]).range([0, width]) 				
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

		var root = fetchTimelineData(store);
		var nodes = [];
		
		for(branch in root){
			for(node in root[branch].values)
				nodes.push(root[branch].values[node]);
		}
		
		var svg = d3.select("#timeline").select("svg")
				.datum(root)
				.attr("height", window_height - minus_timeline)
				.call(chart);

		chart.update();
		nv.utils.windowResize(chart.update);
		chart.dispatch.on('stateChange', function(e) { ('New State:', JSON.stringify(e)); });
		return chart;
	  });
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
			node.push({"office":office_details, "program":program_nm, "Date": build_date, "Date Type": programs[program]["Banner"]});
			
			if(!isInArray(build_date.getTime(), change_dates))
				change_dates.push(build_date.getTime());
		  }
		  	  
		  if(programs[program]["Software File"] != ""){
			  var program_sw_file = getProgramDetails(programs[program]["Software File"]);
			  for (sw_item in program_sw_file){
				var sw_object = program_sw_file[sw_item];
				var modification = getModificationDate(sw_object["New Date"], sw_object["Update Date"]);
				var mod_date = stringToDate(modification["Date"]);

				if(modification["Date"] && (mod_date >= date_start && mod_date <= date_end)){
					if(edge.length < 1){
						edge.push({"Software" : [sw_object["Software"]], "Date Type" : modification["Date Type"], "Date" : mod_date});
						if(!isInArray(mod_date.getTime(), change_dates))
							change_dates.push(mod_date.getTime());
					}
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
							if(project == edge.length - 1){
								edge.push({"Software" : [sw_object["Software"]], "Date Type" : modification["Date Type"], "Date" : mod_date});
								if(!isInArray(mod_date.getTime(), change_dates))
									change_dates.push(mod_date.getTime());
							}
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
						if(!isInArray(mod_date.getTime(), change_dates))
							change_dates.push(mod_date.getTime());
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
							if(project == edge.length - 1){
								edge.push({"Publications" : [pub_object["Title"]], "Date Type" : modification["Date Type"], "Date" : mod_date});
								if(!isInArray(mod_date.getTime(), change_dates))
									change_dates.push(mod_date.getTime());
							}
						}
					}
				}
			  }
		  }
		  
		  if(edge.length != 0)
			node.push({"office":office_details, "program":program_nm, "projects": edge});
		}
		
		root = {"offices": office_checker}; //top level of object - offices

		for (n in node){
			for (r_office in root.offices){
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