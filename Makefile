
run:
	python -m cbd


###############################################################################
# TOOLS
###############################################################################
verif:
	pylint cbd/__main__.py

uml: 
	pyreverse -o png cbd -p cbd
	mkdir -p doc/diagrams
	mv packages_* classes_* doc/diagrams/
