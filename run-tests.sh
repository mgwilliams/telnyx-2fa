#!/bin/sh

pip install -r requirements-test.txt
pytest ./tests
