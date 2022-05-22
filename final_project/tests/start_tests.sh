#!/bin/bash
cd /tests/utils/db;
python setup.py;

cd /tests;
pytest -s -l -v -n "${THREADS:-2}" --alluredir /tmp/allure --selenoid ./ui_tests/;
pytest -s -l -v -n "${THREADS:-2}" --alluredir /tmp/allure ./api_tests/;
