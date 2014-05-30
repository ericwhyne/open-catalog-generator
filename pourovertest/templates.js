var templates = {
	Program: "<h2 class='vis_headers'>{{DARPA Program Name}}</h2><p class='vis_p'>{{Description}}</p>",
	
	Publications: "<h2 class='vis_headers'>{{Title}}</h2><p class='vis_p'><a href='#'>{{Link}}</a></p><div><ul>Teams:{{#Program Teams}}<li>{{.}}</li>{{/Program Teams}}</ul></div><div><ul>Authors:{{#Authors}}<li>{{.}}</li>{{/Authors}}</ul></div>",
	
	Software: "<h2 class='vis_headers'>{{Software}}</h2><p class='vis_p'>{{Description}}<br><a href='#'>{{Public Code Repo}}</a></p><div><ul>Teams:{{#Program Teams}}<li>{{.}}</li>{{/Program Teams}}</ul></div><div><ul>Languages:{{#Languages}}<li>{{.}}</li>{{/Languages}}</ul></div> <div><ul>Licenses:{{#License}}<li>{{.}}</li>{{/License}}</ul></div><div><ul>Categories:{{#Categories}}<li>{{.}}</li>{{/Categories}}</ul></div>",
	
	Licenses: "<h2 class='vis_headers>{{License Long Name}}</h2><br><p class='vis_p'>{{License Description}}<br><a href='#'>{{License Link}}</a><div><ul>Short Names:{{#License Short Name}}<li>{{.}}</li>{{/License Short Name}}</ul></div>",
	
	PublicationsOrdered: "<dd><h2 class='vis_headers'>{{Title}}</h2><p class='vis_p'><a href='#'>{{Link}}</a></p><div><ul>Teams:{{#Program Teams}}<li>{{.}}</li>{{/Program Teams}}</ul></div><div><ul>Authors:{{#Authors}}<li>{{.}}</li>{{/Authors}}</ul></div></dd>",
	
	SoftwareOrdered: "<dd><h2 class='vis_headers'>{{Software}}</h2><p class='vis_p'>{{Description}}<br><a href='#'>{{Public Code Repo}}</a></p><div><ul>Teams:{{#Program Teams}}<li>{{.}}</li>{{/Program Teams}}</ul></div><div><ul>Languages:{{#Languages}}<li>{{.}}</li>{{/Languages}}</ul></div> <div><ul>Licenses:{{#License}}<li>{{.}}</li>{{/License}}</ul></div><div><ul>Categories:{{#Categories}}<li>{{.}}</li>{{/Categories}}</ul></div></dd>",
	
	SoftwareCenter:  "<td><span><h4><a target='blank' href='#'><img src='laptop.png' class='id-image'/></a>{{Software}}</h4></span><p>{{Description}}<br /><br />&nbsp;</p></td>"
};