bumpversion:
	pip install bumpversion

major minor patch: bumpversion
	bumpversion $@
	@echo "push via \`git push origin master --tags\`"

clean:
	rm -rf build/ dist/ *.egg *.egg-info/ .eggs/
	find . -name '*.py[co]' | xargs rm
	find . -name '__pycache__' | xargs rm

test:
	python2.7 setup.py nosetests
