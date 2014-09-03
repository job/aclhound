bumpversion:
	pip install bumpversion

major minor patch: bumpversion
	bumpversion $@
	@echo "push via \`git push origin master --tags\`"

clean:
	find . -name '*.py[co]' | xargs -r rm
	find . -name '__pycache__' | xargs -r rm
	rm -rf build/ dist/ *.egg *.egg-info/

test:
	python2.7 setup.py nosetests
