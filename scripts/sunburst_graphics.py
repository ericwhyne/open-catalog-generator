def sunburst_header():
  return """
  <!DOCTYPE html>
  <html lang='en'><meta http-equiv='Content-Type' content='text/html; charset=utf-8' />
  <link rel='stylesheet' href='style_v2.css' type='text/css'/>
  <link rel='stylesheet' href='banner_style.css' type='text/css'/>
  <link rel='stylesheet' href='css/flick/jquery-ui-1.10.4.custom.css' type='text/css'/>
  <link rel='stylesheet' href='css/list_style.css' type='text/css'/>
  <script type='text/javascript' src='jquery-latest.js'></script>
  <script type="text/javascript" src="templates.js"></script>
  <script type="text/javascript" src="mustache.js"></script>
  <script type="text/javascript" src='d3.min.js'></script>
  <style>
   body{
	overflow-x: hidden;
	overflow: auto;
	background: #E5E4E2;
   }

   h1, h2, h3, h4, h5 {
    max-width:100%;
   }
  </style>
  
"""

def sunburst_html(url):
  html = "<div class='darpa-header'><div class='darpa-header-images darpa-header-images-size'><a href='http://www.darpa.mil/'><img class='darpa-logo' src='darpa-transparent-v2.png'></a><a href='index.html' class='programlink'><img src='Open-Catalog-Single-Big.png'></a></div>"
  html += "<div class='darpa-header-text'><h1 class='no_space'><span><font color='white'> / </font><a href=\"http://www.darpa.mil/Our_Work/I2O/\"' class='programlink programheader programheader-i2o'>Information Innovation Office (I2O) &nbsp/&nbsp</a><a href=\"data_vis.html\"' class='programlink visheader'>Catalog Sunburst Visualization</a></span></h1></div></div>"
  
  html += "<div id = 'sunburst-container'><div id='vis_map'><div class='sunburst-div' id='sunburst'></div></div><div id='vis_view'></div></div>"
  
  return html
def sunburst_script(): 
  return """

<script type='text/javascript'>
var active_programs = new Array();
var window_height = $(window).height();
var window_width = $(window).width();

$( document ).ready(function() {
	var vis_html = getProgramView();
	$('#vis_view').html(vis_html);
	createSunburstGraph('#sunburst');
	$('#vis_view').height($('#vis_map').height());
	
	window.onresize = function () {
		window_height = $(window).height();
		window_width = $(window).width();
		$('#vis_view').empty();
		$('#vis_view').html(getProgramView());
		$("#sunburst").empty();
		createSunburstGraph('#sunburst');
		$('#vis_view').height($('#vis_map').height());		
	};
});

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

function getDetailsNode(data, edges, node_name, size){
	var _details_edge = new Array();
	var _details_node = new Array();
	
	for( edge in edges){

		var values = new Array();
		var _edge = new Array();

		for (i in data) {
			//This is the data for the outermost layer of the graph. Performing a value check in order to prevent duplicates
			for(value in data[i][edges[edge]]){
				var data_value = data[i][edges[edge]][value];
				if(!isInArray(data_value, values)){
					_edge.push({"name": data_value, "size": size});
					values.push(data_value);
				}
			}

			if(i == data.length - 1){
				var _node = "";
				if(edges[edge] == "Program Teams")
					_node = {"name":"Teams", "children": _edge};
				else
					_node = {"name":edges[edge], "children": _edge};
					
				_details_edge.push(_node);
			}
		}
	}
	
	_details_node = {"name":node_name, "children": _details_edge};
	return _details_node;

}

function getProgramLinks(program){
	var links = new Array();
	var link_html = "";
	url_path = window.location.href;
	console.log(url_path);
	url_path = url_path.replace(/\/.+\.html/g, "this.html");
	console.log(url_path);	
	link_html += '<p id="program_templ_links " class="vis_p">';
	if (program['Pubs File'] != "")
		links.push('<a href="#">Publications</a>');
		//links.push('Publications');
	if (program['Software File'] != "")
		//links.push('<a href="#">Software</a>');
		links.push('Software');

	if(links.length > 1){
		$.each(links, function (link) {
			link_html += links[link];
			if(link < links.length - 1)
				link_html += ' | '
		});
	}
	else
		link_html += links[0];

	link_html += '</p>';	
	return link_html;
}

function adjustvisView(query_array){
	  //query_array = typeof query_array == 'string' ? [query_array] : query_array;
	  var html = "";
	  var level_data = new Array();

	  if(query_array.length == 0){
		html = getProgramView();
		$('#vis_view').html(html);
      }
	  else if(query_array.length == 1){

		var program_data = getProgramDetails(query_array[0].toUpperCase() + "-program.json");
		var html = Mustache.to_html(templates.Program, program_data);
		var curr_program = new Array();
		
		$.each(active_programs, function (program) {
				if(active_programs[program]['Program Name'] == query_array[0]){
					 curr_program = active_programs[program];
					 return false;
				}
			});

		html += getProgramLinks(curr_program);	

	  }
	  else if(query_array.length > 1){
		var file_type = "";
		if(query_array[1] == "Software")
			file_type = "software";
		else
			file_type = "pubs";
			
		var program_data = getProgramDetails(query_array[0].toUpperCase() + "-" + file_type + ".json");
		var template = "";

		if(query_array.length == 3){
			if(query_array[1] == "Software"){
				template = templates.SoftwareOrdered;
				program_data.sort(sortByProperty("Software"));
			}
			else if(query_array[1] == "Publications"){
				template = templates.PublicationsOrdered;
				program_data.sort(sortByProperty("Title"));
			}		
		
			for (data in program_data) {
				var child_query = getChildQueryArray(query_array[2], program_data[data]);
				for( child in child_query){
					if(!isInArray(child_query[child], level_data))
						level_data.push(child_query[child]);
					break;
				}
			}
			level_data.sort();
		}
		else{
				if(query_array[1] == "Software"){
					template = templates.Software;
					program_data.sort(sortByProperty("Software"));
				}
				else if(query_array[1] == "Publications"){
					template = templates.Publications;
					program_data.sort(sortByProperty("Title"));
				}
		}

		if(query_array.length == 4){
			var lowest_value = "";
			if(query_array[2] == "Categories")
				lowest_value = "Category";
			else if(query_array[2] == "Teams")
				lowest_value = "Team";
			else
				lowest_value = "License";
		}

		if (query_array.length == 2)
			html = '<h2 class="vis_headers">' + query_array[0] + " " + query_array[1] + '</h2><p class="vis_p">Total Records: ' + program_data.length + '</p><hr><div class="vis_view_scroll">';
		if (query_array.length == 3)
			html = '<h2 class="vis_headers">' + query_array[0] + " " + query_array[1] + ' ordered by '+ query_array[2] +'</h2><p class="vis_p">Total Records: ' + program_data.length + '</p><hr><div class="vis_view_scroll">';
		if (query_array.length == 4)
			html = '<h2 class="vis_headers">' + query_array[0] + " " + query_array[1] + ' - ' + lowest_value + ':' + query_array[3] + '</h2>';			

		if(query_array.length == 3){
			 html += "<dl>";
			 for (var i=0;i < level_data.length;i++){
				var heading = level_data[i] != "" ? level_data[i] : "Undefined " + query_array[2];
				html +="<dt><h2><u>" + heading + "</u></h2></dt>";
				for (data in program_data) {
					var child_query = getChildQueryArray(query_array[2], program_data[data]);
					
					for( child in child_query){
						if(child_query[child] == level_data[i]){
							html += Mustache.to_html(template, program_data[data]);
							break;
						}
					}	
				}
			}
			html += "</dl>";

		}
		else{	
			var match_html = "";
			var match_count = 0;
			for (data in program_data) {	
				if (program_data[data]["Software"] == "")
					program_data[data]["Software"] = "No Name Available";
				if(program_data[data]["Title"] == "")
					program_data[data]["Title"] = "No Name Available";

				if(query_array.length == 4){

					var child_query = getChildQueryArray(query_array[2], program_data[data]);
					for( child in child_query){
						if(child_query[child] == query_array[3]){
							match_count ++;
							match_html += Mustache.to_html(template, program_data[data]);
							break;
						}
					}
					if(data == program_data.length -1){
						html += "<p>Total Records: " + match_count + "</p><hr><div class='vis_view_scroll'>" + match_html;
					}
				}
				else
					html += Mustache.to_html(template, program_data[data]);
			}	
		}
	  }
	html += "</div>";		
	$('#vis_view').html(html);
}

function getProgramView(){
	if(active_programs.length == 0)
		active_programs = getPrograms();
	var html = "<h2 class='vis_headers'>DARPA Programs</h2><p>Total Number of Programs: " + active_programs.length + "</p><hr>";
	html += "<div class='vis_view_scroll'>";
	var template = templates.Program;
	
	active_programs.sort(sortByProperty('Program Name'));
	
	$.each(active_programs, function (program) {
		var program_file = active_programs[program]['Program File'] 
		var program_data = getProgramDetails(program_file);
		html += Mustache.to_html(template, program_data);
		html += getProgramLinks(active_programs[program]);
		
	});
	html += "</div>";
	return html;
}


function getChildQueryArray(query, data){
	var child_query = new Array();
	if(query == "Categories")
		child_query = data.Categories;
	else if(query == "Teams")
		child_query = data["Program Teams"];
	else if(query == "License")
		child_query = data.License;
		
	return child_query;
}

function getSunburstJSON(){
	var _root = new Array();
	var program_data = new Array();
	program_data = getPrograms();

	var sw_edges = ["Program Teams","Categories","License"];
	var pubs_edges = ["Program Teams"];
	var _primary_edge = new Array();
	var _primary_node = new Array();

	program_data.sort(sortByProperty('Program Name'));
	for (program in program_data){
		
		var program_nm = program_data[program]["Program Name"];
		var _program_edge = new Array();
		var _program_node = new Array();
		
		if(program_data[program]["Software File"] != ""){
			var details_node = getDetailsNode(getProgramDetails(program_data[program]["Software File"]), sw_edges, "Software", 2000); 
			_program_edge.push(details_node);
		}
		
		if(program_data[program]["Pubs File"] != ""){
			var details_node = getDetailsNode(getProgramDetails(program_data[program]["Pubs File"]), pubs_edges, "Publications", 3000); 
			_program_edge.push(details_node);
			
		}
		
		_program_node = {"name":program_nm, "children": _program_edge};
		_primary_edge.push(_program_node);
			
	}

	_primary_node = {"name":"DARPA PROGRAMS", "children": _primary_edge};
	_root.push(_primary_node);
	
	var json_string = JSON.stringify(_root, null, '  ');
	json_string = json_string.substring(1, json_string.length - 2);
	json_string = json_string.replace(/"key"/g, '"name"');
	json_string = json_string.replace(/"values"/g, '"children"');
	var json_object = $.parseJSON(json_string);

	return json_object;
}

function createSunburstGraph(div){
	
	var margin = {};
	var graph_top = graph_bottom = graph_left = graph_right = 0;
	
	//calculate the graph margins and radius
	graph_top = graph_bottom = window_height * .40222;
	graph_right = graph_left = window_width * .26042;
	margin = {top: graph_top, right: graph_right, bottom: graph_bottom, left: graph_left}; //bottom and top resizes graph
	var radius = Math.min(margin.top, margin.right, margin.bottom, margin.left);

	var x = d3.scale.linear()
		.range([0, 2 * Math.PI]);

	var y = d3.scale.sqrt()
		.range([0, radius]);

	var color = d3.scale.category20c();

	var svg = d3.select(div).append("svg")
		.attr("width", margin.left + margin.right)
		.attr("height", margin.top + margin.bottom)
	  .append("g")
		  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
 
	var partition = d3.layout.partition()
		.value(function(d) { return d.size; });

	var arc = d3.svg.arc()
		.startAngle(function(d) { var start = Math.max(0, Math.min(2 * Math.PI, x(d.x))); return start; })
		.endAngle(function(d) { var end = Math.max(0, Math.min(2 * Math.PI, x(d.x + d.dx))); return end; })
		.innerRadius(function(d) { var inner = Math.max(0, y(d.y)); return inner;})
		.outerRadius(function(d) { var outer = Math.max(0, y(d.y + d.dy)); return outer; });
	
	var root = getSunburstJSON();
	
	var g = svg.selectAll("g")
	  .data(partition.nodes(root))
		.enter().append("g");

	var tooltip = d3.select("body")
		.append("div")
		.style("position", "absolute")
		.style("z-index", "10")
		.style("color", "black")
		.style("background-color", "#FEFCFF")
		.style("-webkit-border-radius", "10px")
		.style("border", "solid 1 #726E6D")
		.style("visibility", "hidden");
		
	var path = g.append("path")
	  .attr("d", arc)
	  .style("fill", function(d) { return color(( d.children ? d : d.parent).name); })
	  .attr("cursor", function(d){if (d.depth < 2) {return "pointer";}})
	  .attr("title", function(d) { if (d.depth < 2) { var title = ""; d.depth == 0 ? title = "zoom out" : title = d.name; return title; }})
	  .attr("opacity",  function(d) { var opacity = 0; d.depth > 1 ? opacity = 0 : opacity = 1; return opacity; })
      .on("mousemove", function(d){if(isIE() && d.depth < 2){  var text = ""; d.depth == 0 ? text = " zoom out " : text = " " + d.name; return tooltip.text(text).style("top", window.event.y-10 +"px").style("left",window.event.x+10+"px").style("text-align", "center").style("visibility", "visible");}})
	  .on("mouseout", function(){if(isIE()) return tooltip.style("visibility", "hidden");})
	  .on("click", function(d){if (d.depth < 2) click(d);});
	  
	function computeTextRotation(d) { 
	  var angle = x(d.x + d.dx / 2) - Math.PI / 2;
	  var rotate = angle / Math.PI * 180;
	  
	 if( x(d.x + d.dx / 2) > Math.PI)
		rotate = rotate + 180;
		return rotate;
	}
	
	function round(x, n) {
		return Math.round(x * Math.pow(10, n)) / Math.pow(10, n)
	}
	
	function computeAbsolutePlacement(d) { 
		var absolute = y(d.y);

		if( x(d.x + d.dx / 2) > Math.PI)
			absolute = -absolute;
		return absolute;
	}

	function computeAnchor(d, text) { 
		if( x(d.x + d.dx / 2) < Math.PI)
			return "start";
		else
			return "end";
	}

	function computeTransition(d, text) { 
		if(d.depth > 0){
			if( x(d.x + d.dx / 2) == Math.PI){
				if(text.attributes["text-anchor"] == "end")
				return "start";
			}
			else if(x(d.x + d.dx / 2) > Math.PI){
				if(text.attributes["text-anchor"] != "end")
				return "end";	
			}
		}
		else{
			if( x(d.x + d.dx / 2) < Math.PI)
				return "start";
			else
				return "end";
		}
	}	
	  
	var text = g.append("text")
	  .attr("transform", function(d) { var rotate = ""; d.depth == 0 ? rotate = "rotate(0)" : rotate = "rotate(" + computeTextRotation(d) + ")"; return rotate; })
	  .attr("x", function(d) { return computeAbsolutePlacement(d); })
	  .attr("dx", function(d) {var horizontal = ""; d.depth == 0 ? horizontal = "55" :  horizontal = "0"; return horizontal; })
	  .attr("dy", ".35em") // vertical-align
      .attr("text-anchor", function(d) {return computeAnchor(d, this); })
	  .attr("font-size", "75%")
	  .attr("opacity",  function(d) { var opacity = 0; d.depth >= 2 ? opacity = 0 : opacity = 1; return opacity; })
	  .attr("pointer-events", "none")
	  .text(function(d) { return d.name; });

	function click(d) {
	  // fade out all text elements
	  text.transition().attr("opacity", 0);
	  path.transition()
		.duration(250)
		.attrTween("d", arcTween(d))
		.each("end", function(e, i) {
			// check if the animated element's data e lies within the visible angle span given in d

			if (e.x >= d.x && e.x < (d.x + d.dx)) {
			  var dName = d.name, dDepth = d.depth, maxDepth = dDepth + 2;

			  var arcPath = d3.select(this.parentNode).select("path"); //selected path
			  
			  arcPath
				.attr("opacity", function() { var opacity = 0; e.depth < maxDepth ? opacity = 1 : opacity = 0; return opacity; })
				.attr("cursor", function(){if (e.depth < maxDepth) {return "pointer";}})
				.attr("title", function(d) { if (e.depth < maxDepth ) { var title = ""; d.depth == 0 ? title = "zoom out" : title = d.name; return title; }})
				.on("mousemove", function(d){if(isIE() && e.depth < maxDepth ){  var text = ""; d.depth == 0 ? text = " zoom out " : text = " " + d.name; return tooltip.text(text).style("top", window.event.y-10 +"px").style("left",window.event.x+10+"px").style("text-align", "center").style("visibility", "visible");}})
				.on("mouseout", function(){if(isIE() && e.depth < maxDepth ) return tooltip.style("visibility", "hidden");})
				.on("click", function(d){if (e.depth < maxDepth ) click(d);});
				
				//if the start and next points match then the path is closed and text should not be shown
				var pathPoints = arcPath[0][0];
				var start_x = 0, next_x = 0;

				if(isIE()){
					start_x = (pathPoints.getPointAtLength(0).x).toFixed(6);
					next_x = (pathPoints.getPointAtLength(1).x).toFixed(6);
				}
				else{
					start_x = pathPoints.getPointAtLength(0).x;
					next_x = pathPoints.getPointAtLength(1).x;
				}

			  var arcText = d3.select(this.parentNode).select("text");
			  arcText.transition().duration(650)
				.attr("opacity", function(d) {var opacity = 0; if(e.depth < maxDepth && start_x != next_x) { dDepth == 0 ? opacity = 1 : e.name == "DARPA PROGRAMS" ? opacity = 0 : opacity = 1; return opacity;} else return opacity;})
				.attr("transform", function() { var rotate = ""; e.depth == 0 ? rotate = "rotate(0)" : rotate = "rotate(" + computeTextRotation(e) + ")"; return rotate; })
				.attr("x", function(d) { return computeAbsolutePlacement(d); })
				.attr("text-anchor", function(d) {return computeTransition(d, this); });
			}
		});

	   //Updates the data in the right div to reflect the chosen graph path	d
	   var parent_array = new Array();
	   var d_parent = d;
	   for (var i=d.depth;i > 0;i--){
		 parent_array[i-1] = d_parent.name;
		 d_parent = d_parent.parent;
	   }		
		adjustvisView(parent_array);
	}
	
	// Interpolate the scales!
	function arcTween(d) {
	  var xd = d3.interpolate(x.domain(), [d.x, d.x + d.dx]),
		  yd = d3.interpolate(y.domain(), [d.y, 1]),
		  yr = d3.interpolate(y.range(), [d.y ? 20 : 0, radius]);
	  return function(d, i) {
		return i
			? function(t) { return arc(d); }
			: function(t) { x.domain(xd(t)); y.domain(yd(t)).range(yr(t)); return arc(d); };
	  };
	}	
	d3.select(self.frameElement).style("height", margin.top + margin.bottom + "px");
}
</script>
"""