bumpversion:
	pip install bumpversion

major minor patch: bumpversion
	bumpversion $@
	@echo "push via \`git push origin master --tags\`"

clean:
	find . -name '*.py[co]' | xargs rm
	find . -name '__pycache__' | xargs rm
	rm -rf build/ dist/ *.egg *.egg-info/
