
test:
	pytest -vv --pep8 --flakes  demo \
		--cov-report term-missing --cov-report xml --cov demo

clean:
	find . \
		-name '*.pyc' \
		-o -name __pycache__ \
		-o -name .DS_Store \
		| xargs rm -rf

	rm -rf .pytest_cache/ .cache/ .coverage coverage.xml
