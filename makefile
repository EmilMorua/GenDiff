build: #Distribution assembly
    poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install dist/*.whl

