#!/bin/bash

cd /tests
pytest -s -l -v -n "${THREADS:-2}" --alluredir /tmp/allure --selenoid ./ui_tests/
pytest -s -l -v -n "${THREADS:-2}" --alluredir /tmp/allure ./api_tests/