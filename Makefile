TEST = python -m pytest
TEST_ARGS = -s --verbose --color=yes
TYPE_CHECK = mypy --strict --allow-untyped-decorators --ignore-missing-imports
STYLE_CHECK = flake8
COVERAGE = pytest --cov --cov-report term-missing
TARGETS := main.py stratego/*.py

.PHONY: all
all: check-style check-type run-cov run-test clean
	@echo "All checks passed"

.PHONY: check-type
check-type:
	$(TYPE_CHECK) $(TARGETS)

.PHONY: check-style
check-style:
	$(STYLE_CHECK) $(TARGETS)

.PHONY: run-cov
run-cov:
	$(COVERAGE) .

.PHONY: run-test
run-test:
	$(TEST) $(TEST_ARGS) tests

.PHONY: clean
clean:
	# remove all caches recursively
	rm -rf `find . -type d -name __pycache__` # remove all pycache
	rm -rf `find . -type d -name .pytest_cache` # remove all pytest cache
	rm -rf `find . -type d -name .mypy_cache` # remove all mypy cache
	rm -rf `find . -type d -name .hypothesis` # remove all hypothesis cache
	rm -rf `find . -name .coverage` # remove all coverage cache 
