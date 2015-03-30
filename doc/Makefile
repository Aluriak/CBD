SOURCE=report

all: source clean

clean:
	- rm *.aux *.log 

source:
	pdflatex $(SOURCE).tex && pdflatex $(SOURCE).tex
	evince $(SOURCE).pdf

copy_data:
	rm ./data/*.csv
	cp ../data/outputs/*.csv ./data/
	cp ../data/outputs/*.png ./images/


gif:
	- convert -delay 1000 -loop 1 images/hepcidinGraphInteractionsBackground*.png hepcidin_background_interactions.gif
	- convert -delay 1000 -loop 1 images/hepcidinGraphInteractionsNonBackground*.png hepcidin_non_background_interactions.gif
