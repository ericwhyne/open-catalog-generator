OC_DATA_DIR=$(shell pwd)/darpa_open_catalog/
OC_SCRIPTS_DIR=$(shell pwd)/scripts/
OC_TEST_DIR=$(shell pwd)/test/
OC_DEFAULT_TEMPLATE_DIR=$(shell pwd)/templates/simple_sortable_table/
OC_SEARCH_TEMPLATE_DIR=$(shell pwd)/templates/searchable_table/
OC_VIS_TEMPLATE_DIR=$(shell pwd)/templates/sunburst_vis/
OC_BUILD_DIR=$(shell pwd)/build
OC_ACTIVE_CONTENT_FILE=$(shell pwd)/active_content.json
OC_ACTIVE_DEPLOYED_CONTENT_FILE=$(shell pwd)/active_content_deployed.json
OC_LICENSE_CONTENT_FILE=$(OC_DATA_DIR)license-content.json
OC_SCHEMA_FILE=$(OC_DATA_DIR)00-schema-examples.json
CUR_DATE=`date +"%Y-%m-%d"`
CUR_BUILD_DATE=$(OC_BUILD_DIR)/build-date.txt
LAST_BUILD_DATE=$(OC_BUILD_DIR)/last-build-date.txt
NEW_JSON_DIR = $(OC_DATA_DIR)new_json/

website: $(OC_DEFAULT_TEMPLATE_DIR) 
	mkdir -p $(OC_BUILD_DIR)
	cp -r $(OC_DEFAULT_TEMPLATE_DIR)/* $(OC_BUILD_DIR)
	cp -r $(OC_SEARCH_TEMPLATE_DIR)/* $(OC_BUILD_DIR)
	cp -r $(OC_DATA_DIR)/* $(OC_BUILD_DIR)
	cp -r $(OC_VIS_TEMPLATE_DIR)/* $(OC_BUILD_DIR)
	cp $(OC_ACTIVE_CONTENT_FILE) $(OC_BUILD_DIR)
	@if ! test -f $(CUR_BUILD_DATE); then echo $$(($$(date --date="15 days ago" +"%Y%m%d"))) > $(CUR_BUILD_DATE); fi 
	@if test $$(($$(cat $(CUR_BUILD_DATE)))) != $$(($$(date +"%Y%m%d"))); then echo $$(($$(cat $(CUR_BUILD_DATE)))) > $(LAST_BUILD_DATE); echo $$(($$(date +"%Y%m%d"))) > $(CUR_BUILD_DATE); fi
	$(OC_SCRIPTS_DIR)generate_html.py $(OC_ACTIVE_CONTENT_FILE) $(OC_LICENSE_CONTENT_FILE) $(OC_DATA_DIR) $(OC_BUILD_DIR) $(LAST_BUILD_DATE) normallinks

darpawebsite: $(OC_DEFAULT_TEMPLATE_DIR) 
	mkdir -p $(OC_BUILD_DIR)
	cp -r $(OC_DEFAULT_TEMPLATE_DIR)/* $(OC_BUILD_DIR)
	cp -r $(OC_SEARCH_TEMPLATE_DIR)/* $(OC_BUILD_DIR)
	@if ! test -f $(CUR_BUILD_DATE); then echo $$(($$(date --date="15 days ago" +"%Y%m%d"))) > $(CUR_BUILD_DATE); fi 
	@if test $$(($$(cat $(CUR_BUILD_DATE)))) != $$(($$(date +"%Y%m%d"))); then echo $$(($$(cat $(CUR_BUILD_DATE)))) > $(LAST_BUILD_DATE); echo $$(($$(date +"%Y%m%d"))) > $(CUR_BUILD_DATE); fi
	$(OC_SCRIPTS_DIR)generate_html.py $(OC_ACTIVE_CONTENT_FILE) $(OC_LICENSE_CONTENT_FILE) $(OC_DATA_DIR) $(OC_BUILD_DIR)  $(LAST_BUILD_DATE) darpalinks

deploy: $(OC_DEFAULT_TEMPLATE_DIR)
	make clean 
	mkdir -p $(OC_BUILD_DIR)
	cp -r $(OC_DEFAULT_TEMPLATE_DIR)/* $(OC_BUILD_DIR)
	cp -r $(OC_SEARCH_TEMPLATE_DIR)/* $(OC_BUILD_DIR)
	@if ! test -f $(CUR_BUILD_DATE); then echo $$(($$(date --date="15 days ago" +"%Y%m%d"))) > $(CUR_BUILD_DATE); fi 
	@if test $$(($$(cat $(CUR_BUILD_DATE)))) != $$(($$(date +"%Y%m%d"))); then echo $$(($$(cat $(CUR_BUILD_DATE)))) > $(LAST_BUILD_DATE); echo $$(($$(date +"%Y%m%d"))) > $(CUR_BUILD_DATE); fi
	$(OC_SCRIPTS_DIR)generate_html.py $(OC_ACTIVE_DEPLOYED_CONTENT_FILE) $(OC_LICENSE_CONTENT_FILE) $(OC_DATA_DIR) $(OC_BUILD_DIR) $(LAST_BUILD_DATE) darpalinks
	
addjsonfields:$(OC_DEFAULT_TEMPLATE_DIR)
	mkdir -p $(NEW_JSON_DIR)
	$(OC_SCRIPTS_DIR)add_json_fields.py $(OC_ACTIVE_CONTENT_FILE) $(OC_DATA_DIR) $(NEW_JSON_DIR) $(OC_SCHEMA_FILE)

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