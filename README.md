# phabricator-pytest

Attempting Phabricator test in Python.

## Install

```sh
git clone https://github.com/pdehaan/phabricator-pytest.git
cd phabricator-pytest
pipenv install -d
```

## Running tests

```sh
./run.sh
```

## Formatting and linting tests

If you installed the dev dependencies above (using the `-d` flag), running the <kbd>$ ./lint.sh</kbd> script will run both `autopep8` and `pylint`:

```sh
./lint.sh
```
