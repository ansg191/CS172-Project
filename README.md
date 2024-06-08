# CS172 Group 10 Project

## Scraper Instructions

To run the scraper, run the following script:

```bash
./scraper.sh
```

This will run the scraper with the default settings and create a CSV file titled “computerscience_data.csv”
in the current working directory.

The scraper can be configured with environment variables like so:

```bash
SCRAPY_MAX_CONCURRENT_REQUESTS="16" SCRAPY_MAX_FILE_SIZE_GB="1" ./scraper.sh
```

The following environment variables exist:

- `SCRAPY_MAX_FILE_SIZE_GB`
    - Maximum file size in GB before scraper is closed
    - Default: 0.5
- `SCRAPY_MAX_CONCURRENT_REQUESTS`
    - Maximum number of concurrent requests
    - Default: 8
- `SCRAPY_MAX_REQUESTS_PER_DOMAIN`
    - Maximum concurrent requests per domain
    - Default: 4
- `SCRAPY_OUTPUT_FILE`
    - Output CSV File
    - Default: “computerscience_data.csv”

# Server Instructions

The server uses a `flask` backend with `pylucene` to index and query documents and a `React` w/ `TypeScript` frontend.

To run the server, the following dependencies are required:

- `pylucene` - This is difficult to install, so using a docker container is recommended.
- `npm`, `yarn`, or `bun` to compile the React + TypeScript frontend

On start, the server will load `data.csv` in the current directory.
If the lucene index hasn't already been built, it will be constructed from the data in the CSV file.

## Running using Script

With the dependencies installed, the server can be run by executing the following script:
```sh
./server.sh
```

The script will check for the dependencies, compile the frontend, and start the server on port 5000.

## Manually Running

To manually run the server, run the following commands:
```sh
# Enter the web directory
pushd web

# Install JS dependencies (use npm, yarn, or bun here)
npm install

# Build the frontend into the `dist` directory
npm run build

# Return back to repo directory
popd

# Run the server
flask run -h 0.0.0.0 -p 5000
```

## Group Members

| Name                     | SID       | NID      |
|--------------------------|-----------|----------|
| Nikhil Anand Mahendrakar | 862464249 | nmahe008 |
| Anshul Gupta             | 862319580 | agupt109 |
| Ishaan Bijor             | 862128714 | ibijo001 |
| Junbo Yang               | 862234040 | jyang389 |
| Junyan Hou               | 862394589 | jhou038  |
