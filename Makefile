OC_DATA_DIR=$(shell pwd)/darpa_open_catalog/
OC_SCRIPTS_DIR=$(shell pwd)/scripts/
OC_DEFAULT_TEMPLATE_DIR=$(shell pwd)/templates/simple_sortable_table/
OC_BUILD_DIR=$(shell pwd)/build
OC_ACTIVE_CONTENT_FILE=$(shell pwd)/active_content.json
OC_ACTIVE_DEPLOYED_CONTENT_FILE=$(shell pwd)/active_content_deployed.json

website: $(OC_DEFAULT_TEMPLATE_DIR) 
	mkdir -p $(OC_BUILD_DIR)
	cp -r $(OC_DEFAULT_TEMPLATE_DIR)/* $(OC_BUILD_DIR)
	cp -r $(OC_DATA_DIR)/* $(OC_BUILD_DIR)
	$(OC_SCRIPTS_DIR)generate_html.py $(OC_ACTIVE_CONTENT_FILE) $(OC_DATA_DIR) $(OC_BUILD_DIR) normallinks

darpawebsite: $(OC_DEFAULT_TEMPLATE_DIR) 
	mkdir -p $(OC_BUILD_DIR)
	cp -r $(OC_DEFAULT_TEMPLATE_DIR)/* $(OC_BUILD_DIR)
	$(OC_SCRIPTS_DIR)generate_html.py $(OC_ACTIVE_CONTENT_FILE) $(OC_DATA_DIR) $(OC_BUILD_DIR) darpalinks

deployreview: $(OC_DEFAULT_TEMPLATE_DIR) 
	mkdir -p $(OC_BUILD_DIR)
	cp -r $(OC_DEFAULT_TEMPLATE_DIR)/* $(OC_BUILD_DIR)
	cp -r $(OC_DATA_DIR)/* $(OC_BUILD_DIR)
	$(OC_SCRIPTS_DIR)generate_html.py $(OC_ACTIVE_DEPLOYED_CONTENT_FILE) $(OC_DATA_DIR) $(OC_BUILD_DIR) normallinks

clean: $(OC_BUILD_DIR)
	rm -rf $(OC_BUILD_DIR)
