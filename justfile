export PYTHONWARNINGS := "ignore::DeprecationWarning:glycowork"

watch-py:
    watchexec -e py,pyi,toml just test-py check-py

test-py:
    cd lib && uv run pytest

regtest-approve-py:
    cd lib && uv run pytest --regtest-reset

check-py:
    cd lib && uv run mypy .
    cd lib && uv run ruff check
    cd lib && uv run ruff format --check

fmt-py:
    cd lib && uv run ruff format

build-py:
    cd lib && uv build
    cp lib/dist/*.whl web/static/

install-py:
    cd lib && uv pip install -e .

watch-web:
    cd web && bun dev --open
