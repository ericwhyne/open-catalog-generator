#!/usr/bin/python

def filter_head():
  return """
  <!DOCTYPE html>
  <html lang='en'>
  <head>
  <meta http-equiv='Content-Type' content='text/html; charset=utf-8' />
  <title>DARPA - Catalog Filter</title>
  <script type='text/javascript' src='utils.js'></script>
  <script type='text/javascript' src="underscore-min.js"></script>
  <script type='text/javascript' src="pourover.js"></script>
  <script type='text/javascript' src='jquery-latest.js'></script>
  <script type='text/javascript' src='jquery-1.9.1.js'></script>
  <script type='text/javascript' src="jquery-ui.js"></script>
  <script type="text/javascript" src="templates.js"></script>
  <script type="text/javascript" src="mustache.js"></script>
  <script type="text/javascript" src='d3.min.js'></script>
  <script type="text/javascript" src="jkmegamenu.js"></script>
  <link rel="stylesheet" type="text/css" href="css/header_footer.css"/>
  <link rel="stylesheet" type="text/css" href="css/catalog_filter.css"/>
  <link rel='stylesheet' href='css/flick/jquery-ui-1.10.4.custom.css' type='text/css'/> 
  </head>
  
  <body>
"""

def filter_html():
  html = "<header class='darpa-header'><div class='darpa-header-images'><a href='http://www.darpa.mil/'><img class='darpa-logo' src='darpa-transparent-v2.png'></a><a href='index.html' class='programlink'><img src='Open-Catalog-Single-Big.png'></a></div>"
  html += "<div class='darpa-header-text no-space'><span><font color='white'> / </font><a href=\"http://www.darpa.mil/Our_Work/I2O/\"' class='programlink programheader programheader-i2o'>Information Innovation Office (I2O) &nbsp/&nbsp</a><a href=\"catalog_filter.html\"' class='programlink visheader'>Catalog Filter</a></span></div></header>"

  html += """
  <div id='page-content'>
  <br>
  <div id="tabs" class="table-tabs ui-tabs ui-widget ui-widget-content ui-corner-all">
	<ul class="ui-tabs-nav ui-helper-reset ui-helper-clearfix ui-widget-header ui-corner-all" role="tablist">
		<li class="ui-state-default ui-corner-top ui-tabs-active ui-state-active" role="tab" tabindex="0" aria-controls="tabs0" aria-labelledby="ui-id-1" aria-selected="true">
			<a id="ui-id-1" class="ui-tabs-anchor" href="#tabs0" role="presentation" tabindex="-1">Filter All Entries</a>
		</li>
	</ul>
	<div id="program">
		<div id="query_tab" class="ui-tabs-panel ui-widget-content ui-corner-bottom" aria-labelledby="ui-id-1" role="tabpanel" aria-expanded="true" aria-hidden="false">
			<div id="names_title_div" style="float:left; width:10%;"><p>By Program<img class="point-cursor" src="arrow-right.png"  id="name_anchor"/></p></div>
			<div id="names_filter_div" style="float:left; width:90%;"></div>
			<div id="names_menu" style="display:none;" class="megamenu"></div>
			<div style="clear: both;"><HR style="color: #F0FFFF;"></div>
			
			<div id="categories_title_div" style="float:left; width:10%;"><p>By Category<img class="point-cursor" src="arrow-right.png" id="category_anchor"/></p></div>
			<div id="categories_filter_div" style="float:left; width:90%;"></div>
			<div id="categories_menu" style="display:none;" class="megamenu"></div>
			<div style="clear: both;"><HR style="color: #F0FFFF;"></div>
  
			<div id="teams_title_div" style="float:left; width:10%;"><p>By Team<img class="point-cursor" src="arrow-right.png" id="team_anchor"/></p></div>
			<div id="teams_filter_div" style="float:left; width:90%;"></div>
			<div id="teams_menu" style="display:none;" class="megamenu"></div>
			<div style="clear: both;"><HR style="color: #F0FFFF;"></div>
			
			<div id="licenses_title_div" style="float:left; width:10%;"><p>By License<img class="point-cursor" src="arrow-right.png" id="license_anchor"/></p></div>
			<div id="licenses_filter_div" style="float:left; width:90%;"></div>
			<div id="licenses_menu" style="display:none;" class="megamenu"></div>
			<div style="clear: both;"><HR style="color: #F0FFFF;"></div>
		</div>
	</div>
  </div>
  <div id="view" style="height:20px; clear:both;  font-size:13px; font-weight: bold;"><p><span id="results_title" style="float:left;">&nbsp;View Entries</span><img class="point-cursor" style="float:left;" src="arrow-up.gif" id="collection_anchor" name="collection_view" onclick="toggleMenu(this.id, this.name);"/><span id="results_count" style="float:left; padding: 0px 0px 0px 40px;">Loading filter menus...</span></p></div>
  
  <div id="collection_view" class="collectionview" style="display:none;"></div>
  </div>  

  """
  return html
  
def filter_script(): 
  return """
   
  
  <!--[if !IE]><!--><script>  
  if (/*@cc_on!@*/false) {  
	  document.documentElement.className+=' ie10';  
  }  
  </script><!--<![endif]-->  
   
  <script type='text/javascript'>
  var view = [],
	menu_array = {"names":[], "categories":[], "teams":[], "licenses":[""]};
  var programs = getPrograms();	
  var licenses = getLicenses();
  var alphaCharRange = {
		  start: 31, end: 90
  }

  $(document).ready(function() {
		jkmegamenu.definemenu("name_anchor", "names_menu", "mouseover", "query_tab");
		jkmegamenu.definemenu("category_anchor", "categories_menu", "mouseover", "query_tab");
		jkmegamenu.definemenu("team_anchor", "teams_menu", "mouseover", "query_tab");
		jkmegamenu.definemenu("license_anchor", "licenses_menu", "mouseover", "query_tab");
		
		programs.sort(sortByProperty('Program Name'));
  
		var entries = [];
		
		var CaseInsensitiveFilter = PourOver.Filter.extend({
		cacheResults: function(items){
		  var possibilities = this.possibilities,
			  attribute = this.attr;
		
			for(i in items){
				var values = items[i][attribute];
				for (p in possibilities){
					for (value in values){
						if (possibilities[p].value.toLowerCase() === values[value].toLowerCase()) {
						  possibilities[p].matching_cids = PourOver.insert_sorted(possibilities[p].matching_cids,items[i].cid)
						}
					}
				}
			}
		},    
		addCacheResults: function(new_items){
			this.cacheResults.call(this,new_items); 
		},
		getFn: function(query){
			var query_lc = query.toLowerCase(),
				matching_possibility = _(this.possibilities).find(function(p){
					var value_lc = p.value.toLowerCase();
					return value_lc === query_lc;
				});
			return this.makeQueryMatchSet(matching_possibility.matching_cids,query)
		}
	  });
	  
	  var makeCaseInsensitiveFilter = function(name,values,attr){
		var values = _(values).map(function(i){return {value:i}}),
			opts = {associated_attrs: [attr], attr: attr},
			filter = new CaseInsensitiveFilter(name,values,opts);
		return filter;
	  }
	  
	  for (program in programs){
		  var program_nm = programs[program]["Program Name"];
  		
		  if(programs[program]["Software File"] != ""){
			  program_sw_file = getProgramDetails(programs[program]["Software File"]);
  			for (sw_item in program_sw_file){
				var sw_object = program_sw_file[sw_item];
  				entries.push(sw_object);
				createMenuArrays(sw_object["DARPA Program"], "names");
  				createMenuArrays(sw_object["Categories"], "categories");
				createMenuArrays(sw_object["Program Teams"], "teams");
			  }
		  }
  		
		  if(programs[program]["Pubs File"] != ""){
			  program_pub_file = getProgramDetails(programs[program]["Pubs File"])
  			for (pub_item in program_pub_file){
				var pub_object = program_pub_file[pub_item];
  				entries.push(pub_object);
				createMenuArrays(pub_object["DARPA Program"], "names");
  				createMenuArrays(pub_object["Categories"], "categories");
				createMenuArrays(pub_object["Program Teams"], "teams");
			  }
		  }
	  }
 		
	  menu_array["names"].sort();
  	  var name_menu = getQueryMenu(menu_array["names"], "names");
	  $("#names_menu").html(name_menu);
  	
	  menu_array["categories"].sort(insensitive());
  	  var cat_menu = getQueryMenu(menu_array["categories"], "categories");
	  $("#categories_menu").html(cat_menu);
  	
	  menu_array["teams"].sort();
  	  var team_menu = getQueryMenu(menu_array["teams"], "teams");
	  $("#teams_menu").html(team_menu);
	  
	  for (license in licenses){
			var license_object = licenses[license];
			createMenuArrays(license_object["License Short Name"], "licenses");
	  }
	   
	  menu_array["licenses"].sort();
  	  var license_menu = getQueryMenu(menu_array["licenses"], "licenses");
	  $("#licenses_menu").html(license_menu);	   
	  var artifacts_collection = new PourOver.Collection(entries);

	  //create query filters
	  var name_filter = PourOver.makeExactFilter("DARPA Program", menu_array["names"]);
	  var category_filter = makeCaseInsensitiveFilter("Categories", menu_array["categories"], "Categories");
	  var team_filter = makeCaseInsensitiveFilter("Program Teams", menu_array["teams"], "Program Teams");
	  var license_filter = makeCaseInsensitiveFilter("Licenses", menu_array["licenses"], "License");
		
	  artifacts_collection.addFilters([name_filter, category_filter, team_filter, license_filter]);
  	
	  MyView = PourOver.View.extend({
		  selectionFn: function(){

			  var collection = this.collection,
				  name_col = collection.getCurrentFilteredItems("DARPA Program"),
  				  cat_col = collection.getCurrentFilteredItems("Categories"),
				  team_col = collection.getCurrentFilteredItems("Program Teams"),
				  license_col = collection.getCurrentFilteredItems("Licenses");
			  return cat_col.and(team_col).and(name_col).and(license_col);		
		  },
  		render: function(){
			  var items = this.getCurrentItems();
  			  showResults(items);
		  }
	  });
  	
	  view = new MyView("custom_view",artifacts_collection);
  	  view.render();
  });
  
  //gathers all values and puts them in the appropriate place in the menu_array
  function createMenuArrays(argument, type){
	  var entry_array = getStringArray(argument);
	  for(entry in entry_array){
		  if(!isInArray(toCamelCase(entry_array[entry]), menu_array[type])){
			  menu_array[type].push(toCamelCase(entry_array[entry]));
		  }
	  }
  }
  
  function createHeaderArray(query_array){
		var curr_header = '';
		var header_array = [];
		  
		for(query in query_array){
			  for (var i = alphaCharRange.start; i <= alphaCharRange.end; i++) {
				  if (curr_header == '' && query_array[query].charAt(0) == curr_header){
					  if(!isInArray(curr_header, header_array))
						  header_array.push("");
				  }
				curr_header = String.fromCharCode(i);
				  if (query_array[query].charAt(0) == curr_header){
					  if(!isInArray(curr_header, header_array)){
						  header_array.push(curr_header);
					  }
					break;
				  }
			  }
		}
		return header_array;
  }
  
  //creates the html for the Query Menu displayed in the UI
  function getQueryMenu(query_arr, arr_type){
  
	  var curr_header = '';
  	  var menu_html = '<div data-filter-name="' + arr_type + '" data-pourover-filter="makeExactFilter" id="pourover_' + arr_type + '">';
	  var value_cnt = query_arr.length;
  	  var header_cnt = createHeaderArray(query_arr).length;
	  var total_lines = curr_line_cnt = lines_per_column = 0;
  	
	  total_lines = header_cnt + value_cnt;
  	  lines_per_column = Math.ceil(total_lines / 6);
	  
  	  for(query in query_arr){
			
		  if (curr_line_cnt == 0){
			  menu_html += '<div class="column">';
		  }
  		
		  var term = query_arr[query];
  		  var first_letter = term.charAt(0).toUpperCase(); 
		  
  		if (curr_header == '' && first_letter == curr_header){
			  menu_html += '<h3>No Category</h3><ul>';
  			  curr_line_cnt ++;
		  }
  		
		  if (first_letter == curr_header){
			  if(curr_line_cnt == 0)
				  menu_html += '<ul>';
			  //if(first_letter == '') term = '&nbsp;';
  			  menu_html += '<li data-filter-name="' + arr_type + '" data-filter-item-name="'+ term + '" onclick="performQuery(this);" onmouseover="overBackgroundColor(this);" onmouseout="outBackgroundColor(this);">' + term + '</li>';
			  curr_line_cnt ++;
		}
		else{
			for (var i = alphaCharRange.start; i <= alphaCharRange.end; i++) {
				curr_header = String.fromCharCode(i);
				if (first_letter == curr_header){
					menu_html += '</ul><h3>' + first_letter + '</h3><ul>';
					menu_html += '<li data-filter-name="' + arr_type + '" data-filter-item-name="'+ term + '" onclick="performQuery(this);" onmouseover="overBackgroundColor(this);" onmouseout="outBackgroundColor(this);">' + term + '</li>';
					curr_line_cnt = curr_line_cnt + 2;
					break;
				}
			}
		}
		
		if (curr_line_cnt >= lines_per_column){
			menu_html += '</ul></div>';
			curr_line_cnt = 0;
		}
	}	
	
	menu_html += '</ul></div></div></div><div style="clear: both;"></div>';	
	return menu_html;
  }
  
  
  function performQuery(curr_item){
	  var all_selected_items = [];
  	  var result_set = [];
	  var curr_filter = curr_item.attributes['data-filter-name'].value;
  	  var curr_value = curr_item.attributes['data-filter-item-name'].value;
		//console.log(curr_filter);
		//console.log(curr_value);

	  if(curr_value != "clear_filter"){
		  toggleItem(curr_item);
	  }
  	
	  var menu_list = $("#query_tab").find('li');
      menu_list.each(function(li) {
		  if (menu_list[li].selected == true){	
				  if(menu_list[li].attributes['data-filter-name'].value == curr_filter && curr_value == "clear_filter")
					  toggleItem(menu_list[li]);
				  else
					  all_selected_items.push(menu_list[li]);
		  }
	  });

	  var view_names_filter = new PourOver.UI.SimpleSelectElement({filter: view.collection.filters["DARPA Program"]});
  	  var view_cats_filter = new PourOver.UI.SimpleSelectElement({filter: view.collection.filters.Categories});
	  var view_teams_filter = new PourOver.UI.SimpleSelectElement({filter: view.collection.filters["Program Teams"]});
	  var view_licenses_filter = new PourOver.UI.SimpleSelectElement({filter: view.collection.filters["Licenses"]});

	  view_names_filter.filter.clearQuery();
  	  view_cats_filter.filter.clearQuery();
	  view_teams_filter.filter.clearQuery();
	  view_licenses_filter.filter.clearQuery();
  
	  if(all_selected_items.length > 0){
		var n_num = 0, c_num = 0, t_num = 0, l_num = 0;
  		var n_html = '', c_html = '', t_html = '', l_html = '';
		var selected_filter = '', selected_value = '';
  		var open_html = '<ul class="filter-container" style="display: block;">';
		var close_html = '<li class="filter filter-clear point-cursor" onclick="removeFilterValue(this);" data-filter-item-name="clear_filter" data-filter-name="'+ curr_filter + '"><span class="filter-item-title">Clear Filters</span><div class="filter-close-container"><div class="filter-close">&times;</div></div></li></ul>';

		//for (item in all_selected_items){
		$.each(all_selected_items, function (item) {
			selected_filter = all_selected_items[item].attributes['data-filter-name'].value;
			selected_value = all_selected_items[item].attributes['data-filter-item-name'].value;
			//if (selected_value = '&nbsp;') {all_selected_items[item].dataset.filterItemName = '';}

			if(selected_filter == 'names' && n_num == 0){
				//console.log(all_selected_items[item]);
				view_names_filter.filter.query(all_selected_items[item].dataset.filterItemName);
				n_html += open_html;
				n_html += addFilterValue(selected_filter, selected_value);
				n_num++;
			}
			else if (selected_filter == 'names' && n_num > 0){
				view_names_filter.filter.intersectQuery(all_selected_items[item].dataset.filterItemName);
				n_html += addFilterValue(selected_filter, selected_value);
			}
			else if (selected_filter == 'categories' && c_num == 0){
				view_cats_filter.filter.query(all_selected_items[item].dataset.filterItemName);
				c_html += open_html;
				c_html += addFilterValue(selected_filter, selected_value);
				c_num++;
			}
			else if (selected_filter == 'categories' && c_num > 0){
				view_cats_filter.filter.intersectQuery(all_selected_items[item].dataset.filterItemName);
				c_html += addFilterValue(selected_filter, selected_value);
			}
			else if (selected_filter == 'teams' && t_num == 0){
				view_teams_filter.filter.query(all_selected_items[item].dataset.filterItemName);
				t_html += open_html;
				t_html += addFilterValue(selected_filter, selected_value);
				t_num++;
			}
			else if (selected_filter == 'teams' && t_num > 0){
				view_teams_filter.filter.intersectQuery(all_selected_items[item].dataset.filterItemName);
				t_html += addFilterValue(selected_filter, selected_value);
			}
			else if (selected_filter == 'licenses' && l_num == 0){
				view_licenses_filter.filter.query(all_selected_items[item].dataset.filterItemName);
				l_html += open_html;
				l_html += addFilterValue(selected_filter, selected_value);
				l_num++;
			}
			else if (selected_filter == 'licenses' && l_num > 0){
				view_licenses_filter.filter.intersectQuery(all_selected_items[item].dataset.filterItemName);
				l_html += addFilterValue(selected_filter, selected_value);
			}
			
		});
	
		if(curr_value == "clear_filter")
			$("#"+ curr_filter +"_filter_div").html('');
	
		if (n_html != '' && curr_filter == 'names'){ n_html += close_html; $('#names_filter_div').html(n_html);}	
		if (c_html != '' && curr_filter == 'categories'){c_html += close_html; $('#categories_filter_div').html(c_html);}
		if (t_html != ''  && curr_filter == 'teams'){ t_html += close_html; $('#teams_filter_div').html(t_html);}
		if (l_html != ''  && curr_filter == 'licenses'){ l_html += close_html; $('#licenses_filter_div').html(l_html);}			

		var current_queries = [];
		var current_cids = '';

		current_queries.push(view_names_filter.filter.current_query);
		current_queries.push(view_cats_filter.filter.current_query);
		current_queries.push(view_teams_filter.filter.current_query);
		current_queries.push(view_licenses_filter.filter.current_query);
				
		for(query in current_queries){
			if(current_queries[query] != false){
				if(current_cids ==  '')
					current_cids = current_queries[query];
				else
					current_cids = current_cids.and(current_queries[query]);
			}
		}
			
		var ids = current_cids.cids;
		var view_items = view.collection.items;
		
		//console.log(JSON.stringify(ids, null, '  '));
		
		//var result_set = view.collection.get(current_cids.cids); //doesn't work consistently. If you select the same option back to back, it returns nothing. 
		//doing for loop instead
		for (vi in view_items){
			for(id in ids){
				if(view_items[vi].cid == ids[id]){
					result_set.push(view_items[vi]);
					break;
				}
			}
		}
		//console.log(result_set);

		showResults(result_set);		
		if(result_set.length == 0)
			alert("No Results Found");

	}
	else{
		showResults(view.collection.items);
		$("#names_filter_div").html('');
		$("#categories_filter_div").html('');
		$("#teams_filter_div").html('');
		$("#licenses_filter_div").html('');
	}
  }
  
  
  function showResults(items){
  
	  var html = "<table id='collection_table' style='width:100%'><tbody><tr>";
	  var row_count = 0;

  	  items.sort(sortByMultipleProperties('Software','Title'));
	
	  for (var i = 0; i <= items.length; i++) {	
		  if (i < items.length){
			  if(typeof(items[i].Software) == "undefined")
				  html += Mustache.to_html(templates.PublicationsCenter, items[i]);
			  else
				  html += Mustache.to_html(templates.SoftwareCenter, items[i]);
  			
		  }
  		if (i%4 == 3){
			row_count ++;
			if(row_count == 3)
				html += "</tr><tr class='closed_rows'>";
			else
				html += "</tr><tr>";
		}
		
	  }
  	
	  html += "</tr></tbody></table>";
  	  $("#collection_view").html(html);
	  $("#results_count").html("Total: " + items.length);
  }
  
  function overBackgroundColor(item){
	  if (item.style.backgroundColor == 'transparent' ||  item.style.backgroundColor == '')
		  item.style.backgroundColor = '#B7CEEC';
  }
  
  function outBackgroundColor(item){
	  if(item.style.backgroundColor != 'gold') 
		  item.style.backgroundColor = 'transparent';
  	 
  }
  
  function insensitive(){
	  return function(s1, s2) {
	    var s1lower = s1.toLowerCase();
  	  var s2lower = s2.toLowerCase();
	    return s1lower > s2lower? 1 : (s1lower < s2lower? -1 : 0);
	  };
  }
  
  function toCamelCase(str) {
	  return str.replace(/(?:^|\s)\w/g, function(match) {
		  return match.toUpperCase();
	  });
  }
  
  function toggleMenu(arrow_id, arrow_name){
		if($("#" + arrow_name).css("display") == "none"){
		  $("#" + arrow_id).attr("src", "arrow-down.gif");
		  $("#" + arrow_name).attr("style", "clear: both; display:visible;");
		}
		else{
		  $("#" + arrow_id).attr("src", "arrow-up.gif");
		  $("#" + arrow_name).attr("style", "clear: both; display:none;");
		} 
  }
  
  function toggleItem(item){
	  if (item.selected == true)
		  item.selected = false;
	  else
		  item.selected = true;
   
	  if(item.style.backgroundColor != 'gold')
		  item.style.backgroundColor ='gold';
	  else
		  item.style.backgroundColor ='transparent';
  }
  
  function addFilterValue(filter, value){
      //if (value == '') value = '&nbsp;';
	  html = '<li class="filter filter-value point-cursor" onclick="removeFilterValue(this);" data-filter-item-name="' + value + '" data-filter-name="' + filter + '"><span class="filter-item-title">' + value + '</span><div class="filter-close-container"><div class="filter-close">&times;</div></div></li>';
	  
  	  return html;
  }
  
  function removeFilterValue(filter){
  	  var selected_filter = filter.attributes['data-filter-name'].value;
	  var selected_value = filter.attributes['data-filter-item-name'].value;
  	  //if (selected_value == '&nbsp;') selected_value = '';
	  
	  if(selected_value != 'clear_filter'){
		  var filter_list = $("#" + selected_filter + "_filter_div").find('li');
  
		  filter_list.each(function(li) {
			  if (filter_list[li].attributes['data-filter-item-name'].value == selected_value){
				  $("#" + selected_filter + "_filter_div li").eq(li).remove();
  				if(filter_list.length == 2){
					  $("#" + selected_filter + "_filter_div li").remove();
				  }
  				
				  var item_list = $("#pourover_" + selected_filter).find('li');
  				  item_list.each(function(item) {
					  if(item_list[item].attributes['data-filter-item-name'].value == selected_value){
						  performQuery(item_list[item]);
  						return false;
  
					  }
				  });	
			  }
		  });		
	  }
  	  else{
		  $("#" + selected_filter + "_filter_div li").remove();
  		performQuery(filter);
	  }
  }
  
</script>
"""