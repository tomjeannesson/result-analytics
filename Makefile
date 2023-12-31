test:
	python3 -m unittest result_analytics.tests -v

coverage:
	coverage run -m unittest result_analytics.tests -v
	coverage report -m
	coverage html

coverage_open: coverage
	open htmlcov/index.html

download:
	python3 -m unittest result_analytics.tests.moguls.test_mogul_scrapper -v
