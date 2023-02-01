# Gin-config + Absl Command Line interface (GACL)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Simple command-line interface using [abseil](https://github.com/abseil/abseil-py) to parse [gin-config](https://github.com/google/gin-config) files and run configured `main` functions.

## Setup

```bash
git clone https://github.com/jackd/gacl.git
cd gacl
pip install -e .
```

## Example

```bash
cd examples/calculator
python -m gacl add-config.gin params.gin
# 3 + 4 = 7
python -m gacl mul-config.gin params.gin
# 3 * 4 = 12
python -m gacl mul-config.gin params.gin --bindings="x = 5"
# 5 * 4 = 20
```

## Pre-commit

This package uses [pre-commit](https://pre-commit.com/) to ensure commits meet minimum criteria. To Install, use

```bash
pip install pre-commit
pre-commit autoupdate
pre-commit install
```

This will ensure git hooks are run before each commit. While it is not advised to do so, you can skip these hooks with

```bash
git commit --no-verify -m "commit message"
```
