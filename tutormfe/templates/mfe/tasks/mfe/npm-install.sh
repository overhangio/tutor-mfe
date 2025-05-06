#!/bin/bash

if [ "$NODE_ENV" != "development" ]; then
    echo "This script is intended to run only in the development environment."
    exit
fi

# Paths for the fingerprint and package-lock.json
FINGERPRINT_FILE="node_modules/.fingerprint"
PACKAGE_LOCK="package-lock.json"

# Function to generate the SHA1 hash of the package-lock.json file
generate_fingerprint() {
  sha1sum "$PACKAGE_LOCK" | awk '{print $1}'
}

# If node_modules directory is missing, install dependencies
if [ ! -d "node_modules" ]; then
  echo "⚠️  node_modules not found! Installing dependencies..."
  npm clean-install

# If fingerprint file is missing, assume packages may be out of sync and reinstall
elif [ ! -f "$FINGERPRINT_FILE" ]; then
  echo "⚠️  Fingerprint file not found! Re-installing dependencies..."
  npm clean-install

# If both node_modules and fingerprint file exist, compare fingerprints
else
  CURRENT_FINGERPRINT=$(generate_fingerprint)
  STORED_FINGERPRINT=$(cat "$FINGERPRINT_FILE")

  # Reinstall if package-lock.json has changed
  if [ "$CURRENT_FINGERPRINT" != "$STORED_FINGERPRINT" ]; then
    echo "⚠️  package-lock.json changed! Re-installing dependencies..."
    npm clean-install
  else
    # Everything is up to date
    echo "✅ Dependencies are up to date."
    exit 0
  fi
fi


# Store the new fingerprint after installation
generate_fingerprint > "$FINGERPRINT_FILE"
echo "✅ Dependencies installed and fingerprint updated."