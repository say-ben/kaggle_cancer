rm -f requirements.txt
pip freeze > requirements_current.txt
diff --side-by-side --suppress-common-line requirements_current.txt requirements_initial.txt | tr -d "[:blank:]" | tr -d "<" > requirements.txt
rm requirements_current.txt