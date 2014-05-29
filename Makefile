OC_DATA_DIR=$(shell pwd)/darpa_open_catalog/
OC_SCRIPTS_DIR=$(shell pwd)/scripts/
OC_TEST_DIR=$(shell pwd)/test/
OC_METRICS_DIR=$(shell pwd)/metrics_log/
OC_DEFAULT_TEMPLATE_DIR=$(shell pwd)/templates/simple_sortable_table/
OC_SEARCH_TEMPLATE_DIR=$(shell pwd)/templates/searchable_table/
OC_VIS_TEMPLATE_DIR=$(shell pwd)/templates/sunburst_vis/
OC_BUILD_DIR=$(shell pwd)/build
OC_ACTIVE_CONTENT_FILE=$(shell pwd)/active_content.json
OC_ACTIVE_DEPLOYED_CONTENT_FILE=$(shell pwd)/active_content_deployed.json
OC_LICENSE_CONTENT_FILE=$(OC_DATA_DIR)/license-content.json
CUR_DATE=`date +"%Y-%m-%d"`

website: $(OC_DEFAULT_TEMPLATE_DIR) 
	mkdir -p $(OC_BUILD_DIR)
	cp -r $(OC_DEFAULT_TEMPLATE_DIR)/* $(OC_BUILD_DIR)
	cp -r $(OC_SEARCH_TEMPLATE_DIR)/* $(OC_BUILD_DIR)
	cp -r $(OC_DATA_DIR)/* $(OC_BUILD_DIR)
	cp -r $(OC_VIS_TEMPLATE_DIR)/* $(OC_BUILD_DIR)
	cp $(OC_ACTIVE_CONTENT_FILE) $(OC_BUILD_DIR)
	$(OC_SCRIPTS_DIR)generate_html.py $(OC_ACTIVE_CONTENT_FILE) $(OC_LICENSE_CONTENT_FILE) $(OC_DATA_DIR) $(OC_BUILD_DIR) normallinks

darpawebsite: $(OC_DEFAULT_TEMPLATE_DIR) 
	mkdir -p $(OC_BUILD_DIR)
	cp -r $(OC_DEFAULT_TEMPLATE_DIR)/* $(OC_BUILD_DIR)
	cp -r $(OC_SEARCH_TEMPLATE_DIR)/* $(OC_BUILD_DIR)
	$(OC_SCRIPTS_DIR)generate_html.py $(OC_ACTIVE_CONTENT_FILE) $(OC_LICENSE_CONTENT_FILE) $(OC_DATA_DIR) $(OC_BUILD_DIR) darpalinks

deploy: $(OC_DEFAULT_TEMPLATE_DIR)
	make clean 
	mkdir -p $(OC_BUILD_DIR)
	cp -r $(OC_DEFAULT_TEMPLATE_DIR)/* $(OC_BUILD_DIR)
	cp -r $(OC_SEARCH_TEMPLATE_DIR)/* $(OC_BUILD_DIR)
	$(OC_SCRIPTS_DIR)generate_html.py $(OC_ACTIVE_DEPLOYED_CONTENT_FILE) $(OC_LICENSE_CONTENT_FILE) $(OC_DATA_DIR) $(OC_BUILD_DIR) darpalinks

graph: $(OC_DEFAULT_TEMPLATE_DIR) 
	$(OC_SCRIPTS_DIR)generate_graphviz.py $(OC_ACTIVE_CONTENT_FILE) $(OC_DATA_DIR) $(OC_BUILD_DIR) normallinks
	
clean: $(OC_BUILD_DIR)
	rm -rf $(OC_BUILD_DIR)

datainit:
	git clone https://github.com/ericwhyne/darpa_open_catalog.git

dataupdate:
	./update

linkchecker:
	$(OC_TEST_DIR)linkchecker.sh $(OC_BUILD_DIR)/linkcheck.html $(OC_BUILD_DIR)/index.html

deployzip:
	zip -r xdata_catalog_$(CUR_DATE).zip $(OC_BUILD_DIR)/

datatest:
	$(OC_SCRIPTS_DIR)test-cross-site-scripting.py $(OC_DATA_DIR)

metrics:
	$(OC_SCRIPTS_DIR)metrics.py $(OC_ACTIVE_CONTENT_FILE) $(OC_ACTIVE_DEPLOYED_CONTENT_FILE) $(OC_DATA_DIR) $(OC_METRICS_DIR)

