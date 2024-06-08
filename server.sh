#!/usr/bin/env bash

# Check that pylucene is installed
pip show lucene &> /dev/null
if [ $? -ne 0 ]; then
    echo "pylucene is not installed."
    echo "It cannot be installed via pip, so you must install it manually."
    echo "Install it manually to continue..."
    echo "Or run this script inside a docker container/devcontainer provided in the repository."
    exit 1
fi

# Install the required packages
python3 -m pip install -r requirements.txt

# Check whether npm, yarn, or bun is installed
if ! command -v npm &> /dev/null && ! command -v yarn &> /dev/null && ! command -v bun &> /dev/null; then
    echo "npm, yarn, or bun is not installed."
    echo "Please install one of them to continue..."
    exit 1
fi

# Build the frontend
pushd web
if command -v bun &> /dev/null; then
    bun install
    bun run build
elif command -v npm &> /dev/null; then
    npm install
    npm run build
else
    yarn install
    yarn run build
fi
popd

# Run the server
flask run -h 0.0.0.0
