export PYTHONWARNINGS := "ignore::DeprecationWarning:glycowork"

# Watchers =====================================================================

watch-py:
    watchexec -e py,pyi,toml just test-py check-py

watch-web:
    cd web && bun dev --open

# Shared Runners ===============================================================

test: test-py

check: check-py check-web

format: format-py format-web

build: build-py build-web

install: install-py install-web

# Python Runners ===============================================================

test-py:
    cd lib && uv run pytest

regtest-approve-py:
    cd lib && uv run pytest --regtest-reset

check-py:
    cd lib && uv run ruff format --check
    cd lib && uv run mypy .
    cd lib && uv run ruff check

format-py:
    cd lib && uv run ruff format

build-py:
    cd lib && uv build
    cp lib/dist/*.whl web/static/

install-py:
    cd lib && uv pip install -e .

document-py:
    -rm -r web/static/docs/
    cd lib && uv run pdoc --html src/glam -o ../web/static/docs/

# Web Runners ==================================================================

check-web:
    cd web && bun check
    cd web && bun lint

format-web:
    cd web && bun format
    
build-web:
    cd web && bun run build

install-web:
    cd web && bun install

# CI Runners ===================================================================

ci: test check

ci-pages: install document-py build
