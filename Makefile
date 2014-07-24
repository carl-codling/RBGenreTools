SCHEMA_DIR = /usr/share/glib-2.0/schemas/
USER_PLUGIN_DIR = ~/.local/share/rhythmbox/plugins/
SYSTEM_PLUGIN_DIR = /usr/lib/rhythmbox/plugins/
SYSTEM64_PLUGIN_DIR = /usr/lib64/rhythmbox/plugins/

install: schema locales
	@echo "Installing plugin files to $(USER_PLUGIN_DIR) ..."
	@mkdir -p $(USER_PLUGIN_DIR)
	@rm -r -f $(USER_PLUGIN_DIR)RBGenreTools/
	@cp ./RBGenreTools.plugin $(USER_PLUGIN_DIR)
	@cp ./RBGenreTools.py $(USER_PLUGIN_DIR)
	@cp ./RBGenreToolsQLToolsMenu.py $(USER_PLUGIN_DIR)
	@cp ./RBGenreToolsQueueToolsMenu.py $(USER_PLUGIN_DIR)
	@cp ./RBGenreToolsQuicklinks.py $(USER_PLUGIN_DIR)
	@cp ./RBGenreToolsTree.py $(USER_PLUGIN_DIR)
	@cp ./ConfigDialog.py $(USER_PLUGIN_DIR)
	@cp ./quicklinks.json $(USER_PLUGIN_DIR)
	@echo "Done!"

install-systemwide: schema locales
	@if [ -d "$(SYSTEM_PLUGIN_DIR)rb" ]; then \
		echo "Installing plugin files to $(SYSTEM_PLUGIN_DIR) ..."; \
		sudo rm -r -f $(SYSTEM_PLUGIN_DIR)RBGenreTools/; \
		sudo cp -r ./RBGenreTools/ $(SYSTEM_PLUGIN_DIR); \
	else \
		echo "Installing plugin files to $(SYSTEM64_PLUGIN_DIR) ..."; \
		sudo rm -r -f $(SYSTEM64_PLUGIN_DIR)RBGenreTools/; \
		sudo cp -r ./RBGenreTools/ $(SYSTEM64_PLUGIN_DIR); \
	fi
	@echo "Done!"#

schema:
	@echo "Installing schema..."
	@sudo cp ./org.gnome.rhythmbox.plugins.RBGenreTools.gschema.xml $(SCHEMA_DIR)
	@sudo glib-compile-schemas $(SCHEMA_DIR)
	@echo "... done!"


uninstall:
	@echo "Removing schema file..."
	@sudo rm -f $(SCHEMA_DIR)org.gnome.rhythmbox.plugins.RBGenreTools.gschema.xml
	@echo "Removing plugin files..."
	@rm -r -f $(USER_PLUGIN_DIR)RBGenreTools/
	@sudo rm -r -f $(SYSTEM_PLUGIN_DIR)RBGenreTools/
	@sudo rm -r -f $(SYSTEM64_PLUGIN_DIR)RBGenreTools/
	@echo "Done!"
	

	


