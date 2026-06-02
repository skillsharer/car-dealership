#!/usr/bin/env bash

set -euo pipefail

rm -rf build dist
mkdir -p build/package dist

uv pip install \
  --python .venv/bin/python \
  --target build/package \
  --python-platform x86_64-manylinux2014 \
  --python-version 3.12 \
  --only-binary=:all: \
  "pandas>=2.2.3"

cp src/*.py build/package/

cd build/package
zip -r ../../dist/lambda.zip . \
  -x "*.pyc" \
  -x "*/__pycache__/*"

cd ../..

echo "Created dist/lambda.zip"