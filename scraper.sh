#!/usr/bin/env bash

# Install the required packages
python3 -m pip install -r requirements.txt

# Set settings
export SCRAPY_MAX_FILE_SIZE_GB="0.5"
export SCRAPY_MAX_CONCURRENT_REQUESTS="8"
export SCRAPY_MAX_REQUESTS_PER_DOMAIN="4"
export SCRAPY_OUTPUT_FILE="computerscience_data.csv"

# Run the scraper
python3 scraper.py
