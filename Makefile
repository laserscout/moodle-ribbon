
exam := quiz

header := exam-2020-6

####

ifeq ($(USER),nikos)
	python := /usr/local/bin/python3
	ribbon := ~/projects//moodle-ribbon.git/trunk
else
	python := /usr/local/bin/python3
	ribbon := ~/Workspace//moodle-ribbon
endif

pandoc := pandoc --pdf-engine=xelatex -V header-includes:'\setromanfont{Times New Roman} \setmonofont{Menlo}'

#### Rules


ribbon:
	$(python) $(ribbon)/ribbon.py $(exam).md $(exam).gift -p $(header)

report:
	$(pandoc) $(exam).md -o $(exam).pdf

clean:
	rm -rf $(exam).pdf $(exam).gift *.xml *~

up:
	svn up
