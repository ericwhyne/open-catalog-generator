def sunburst_header():
  header = "<div class='darpa-header'><a href='http://www.darpa.mil/'><img class='darpa-logo' src='darpa-transparent-v2.png'></a><h1><a href='index.html' class='programlink'><img class='catalog-logo' src='Open-Catalog-Single-Big.png'></a>"
  header += "<span><font color='white'> / </font><a href=\"http://www.darpa.mil/Our_Work/I2O/\"' class='programlink programheader'>Information Innovation Office (I2O)</a></span></h1>"
  
  
  header += "</div>"
  return header
  

def sunburst_html():
  return """
<div id='ontology'>
	<div id='ontology_map' style='width:59%; float:left; margin_left:5px; background:#E5E4E2; border: 2px solid #87AFC7; min-height:1100px;'>
		<div class="sunburst-div" id="sunburst" style='width:98%; height:100px;'></div>
	</div>
	<div id='ontology_view' style='width:40.68%; float:left; background:#E6EEEE; border: 2px solid #87AFC7; border-left: 0px; min-height:1100px;'>
	</div>
</div>
"""

def sunburst_script(): 
  return """
<html>
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
height: 1100px;
overflow:auto;
}
</style>
<script type='text/javascript'>
$( document ).ready(function() {
	var ontology_html = getProgramView();
	
	$('#ontology_view').html(ontology_html);
	adjustHeight();
	
	createSunburstGraph('#sunburst');
	$(window).scroll(function(){
	  var top_margin = '';
	  if(isIE())
		top_margin = $(window).scrollTop() < getScrollHeight() ? $(window).scrollTop() : getScrollHeight();
	  else
		top_margin = $(window).scrollTop() < getScrollHeight() ? $(window).scrollTop() : getScrollHeight();

	  $("#sunburst").stop().animate({"margin-top": (top_margin) + "px", "margin-left":"0px"}, "slow" );
	});
});

var active_programs = [];

function getPrograms() {
	console.log("get programs");
	var programs;
	$.ajax({
		async: false,
		url: 'active_content.json',
		dataType: 'json',
		success: function(response){
		   programs = response;
		}
	});
	
	console.log(programs);
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
  return array.indexOf(value) > -1;
}


function isIE() {
	var ua = window.navigator.userAgent;
	var msie = ua.indexOf("MSIE ");

	if (msie > 0)      
		return true;
	else    // If another browser, return false
		return false;
}

function sortByProperty(property) {
    return function (a, b) {
        var sortStatus = 0;
        if (a[property] < b[property]) {
            sortStatus = -1;
        } else if (a[property] > b[property]) {
            sortStatus = 1;
        }
 
        return sortStatus;
    };
}

function adjustHeight(){
	window.scrollTo(0,0);
	$("#sunburst").stop().animate({"margin-top":"0px", "margin-left":"0px"}, "slow" );
	$("#sunburst").css( {"margin-top":"0px", "margin-left":"0px"} );
	$("#ontology_map").height($("#ontology_view").height());

	$(document).resize(function() {
		//alert("doc size: " + $(document).height());//changes - needs to be adjusted
		//alert("doc body scroll: " + document.body.scrollTop); //set to 0
		//var height = window_height + 300;
		//$(document).height(height);
		//$(document).height = height;
		//$(document).css('height', '100');
		//alert("map scroll height: " + $("#ontology_map")[0].scrollHeight); //adjusted by function, correct scrolling

		 //   var objDiv = $("#ontology_map");
		//var iScrollHeight = objDiv.prop("scrollHeight");
		//objDiv.prop("scrollTop", 120); 
		//$("#ontology_map").empty().append(objDiv.innerHTML);
		
	});
	
	
	//$(document).trigger('resize');
	//alert("height after: " + $(document).height());

}

function getScrollHeight(){
	var map_height = $('#ontology_map').height();

	if(isIE()){
		if(map_height > 1007)
			return map_height - 1007;
		else
			return 100;
	}
	else{
		if(map_height > 1100)
			return map_height - 645;
		else
			return 100;
	}
}


function getDetailsNode(data, edges, node_name, size){
	var _details_edge = new Array();
	var _details_node = new Array();
	
	for( edge in edges){

		var values = new Array();
		var _edge = new Array();

		for (i in data) {
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
	var links = [];
	var link_html = "";
	console.log(program);
	link_html += '<p id="program_templ_links " class="vis_p">';
	if (program['Pubs File'] != "")
		//links.push('<a href="#">Publications</a>');
		links.push('Publications');
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

function adjustOntologyView(query_array){

	  query_array = typeof query_array == 'string' ? [query_array] : query_array;
	  //console.log(query_array);
	  var html = "";
	  var level_data = [];
	  if(query_array.length == 0){
		html = getProgramView();
      }
	  else if(query_array.length == 1){
		var program_data = getProgramDetails(query_array[0] + "-program.json");
		
		html = Mustache.to_html(templates.Program, program_data);
		html += getProgramLinks(active_programs[program]);	
	  }
	  else if(query_array.length > 1){
		var file_type = "";
		if(query_array[1] == "Software")
			file_type = "software";
		else
			file_type = "pubs";
			
		var program_data = getProgramDetails(query_array[0] + "-" + file_type + ".json");
		var template = "";

		if(query_array[1] == "Software"){
			template = templates.Software;
			program_data.sort(sortByProperty("Software"));
		}
		else if(query_array[1] == "Publications"){
			template = templates.Publications;
			program_data.sort(sortByProperty("Title"));
		}

		if(query_array.length == 3){
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
			html = '<h1 class="vis_headers">' + query_array[0] + " " + query_array[1] + ':</h1><p class="vis_p">Total Records: ' + program_data.length + '</p>';
		if (query_array.length == 3)
			html = '<h1 class="vis_headers">' + query_array[0] + " " + query_array[1] + ' ordered by '+ query_array[2] +':</h1><p class="vis_p">Total Records: ' + program_data.length + '</p>';
		if (query_array.length == 4)
			html = '<h1 class="vis_headers">' + query_array[0] + " " + query_array[1] + ' - ' + lowest_value + ' \"' + query_array[3] + '\":</h1>';			



		if(query_array.length == 3){
			 for (var i=0;i < level_data.length;i++){
				var heading = level_data[i] != "" ? level_data[i] : "Undefined " + query_array[2];
				html +="<h2><u>" + heading + "</u></h2>";
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
							console.log("match");
							match_count ++;
							match_html += Mustache.to_html(template, program_data[data]);
							break;
						}
					}
					if(data == program_data.length -1){
						html += "<p class='vis_p'>Total Records: " + match_count + "</p>" + match_html;
					}
				}
				else
					html += Mustache.to_html(template, program_data[data]);
			}	
		}
	  }

	$('#ontology_view').html(html);
	adjustHeight();
}

function getProgramView(){
	if(active_programs.length == 0)
		active_programs = getPrograms();
	var html = "<h1 class='vis_headers'>DARPA Programs</h1><p class='vis_p'>Total Number of Programs: " + active_programs.length + "</p>";
	var template = templates.Program;
	
	active_programs.sort(sortByProperty('Program Name'));
	
	$.each(active_programs, function (program) {
		var program_nm = active_programs[program]['Program Name']
		var program_data = getProgramDetails(program_nm + "-program.json");
		html += Mustache.to_html(template, program_data);
		html += getProgramLinks(active_programs[program]);
		
	});
	return html;
}


function getChildQueryArray(query, data){
	var child_query = [];
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
			var details_node = getDetailsNode(getProgramDetails(program_data[program]["Software File"]), sw_edges, "Software", 3000); 
			_program_edge.push(details_node);
		}
		
		
		if(program_data[program]["Pubs File"] != ""){
			var details_node = getDetailsNode(getProgramDetails(program_data[program]["Pubs File"]), pubs_edges, "Publications", 2000); 
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
	
	if(isIE())
		margin = {top: 480, right: 500, bottom: 300, left: 520};
	else
		margin = {top: 360, right: 540, bottom: 280, left: 460};
	
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
		.startAngle(function(d) { var start = Math.max(0, Math.min(2 * Math.PI, x(d.x))); d.depth == 0 ?  start = Math.max(0, Math.min(2 * Math.PI, (x(d.x) - 100))) : start; return start; })
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
	  .attr("cursor", "pointer")
	  .style("fill", function(d) { return color(( d.children ? d : d.parent).name); })
	  .attr("title", function(d) { var title = ""; d.depth == 0 ? title = "zoom out" : title = d.name; return title; })
      .on("mousemove", function(d){if(isIE()){  var text = ""; d.depth == 0 ? text = " zoom out " : text = " " + d.name; return tooltip.text(text).style("top", window.event.y-10 +"px").style("left",window.event.x+10+"px").style("text-align", "center").style("visibility", "visible");}})
	  .on("mouseout", function(){if(isIE()) return tooltip.style("visibility", "hidden");})
	  .on("click", click);
	  
	function computeTextRotation(d) { 
	  var angle = x(d.x + d.dx / 2) - Math.PI / 2;
	  var rotate = angle / Math.PI * 180;
	  
	 if( x(d.x + d.dx / 2) > Math.PI)
		rotate = rotate + 180;

	  return rotate;
	}
	
	function computeAbsolutePlacement(d) { 
	  var absolute = y(d.y);
	  
	 if( x(d.x + d.dx / 2) > Math.PI)
	   absolute = -(y(d.y));
	  

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
	  .attr("font-size", isIE() ? "90%" : "75%")
	  .attr("pointer-events", "none")
	  .text(function(d) { return d.name; });

	function click(d) {
	  // fade out all text elements
	  text.transition().attr("opacity", 0);
		  
	  path.transition()
		.duration(750)
		.attrTween("d", arcTween(d))
		.each("end", function(e, i) {
			// check if the animated element's data e lies within the visible angle span given in d
			if (e.x >= d.x && e.x < (d.x + d.dx)) {
			  var arcText = d3.select(this.parentNode).select("text");
			  // fade in the text element and recalculate positions
			  arcText.transition().duration(750)
				.attr("opacity", 1)
				.attr("transform", function() { var rotate = ""; e.depth == 0 ? rotate = "rotate(0)" : rotate = "rotate(" + computeTextRotation(e) + ")"; return rotate; })
				.attr("x", function(d) { return computeAbsolutePlacement(d) ; })
				.attr("text-anchor", function(d) {return computeTransition(d, this); })
			}
		});

	   var parent_array = [];
	   var d_parent = d;
	   for (var i=d.depth;i > 0;i--){
		 parent_array[i-1] = d_parent.name;
		 d_parent = d_parent.parent;
	   }		
		adjustOntologyView(parent_array);
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