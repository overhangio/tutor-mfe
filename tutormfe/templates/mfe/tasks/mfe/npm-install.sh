#!/bin/bash

# Paths for the fingerprint and package-lock.json
FINGERPRINT_FILE="node_modules/.fingerprint"
PACKAGE_LOCK="package-lock.json"

# Function to generate the SHA1 hash of the package-lock.json file
generate_fingerprint() {
  sha1sum "$PACKAGE_LOCK" | awk '{print $1}'
}

# Check if node_modules exists and fingerprint is valid
if [ ! -d "node_modules" ]; then
  echo "⚠️  node_modules not found! Installing dependencies..."
  npm clean-install

elif [ ! -f "$FINGERPRINT_FILE" ]; then
  echo "⚠️  Fingerprint file not found! Re-installing dependencies..."
  npm clean-install

else
  CURRENT_FINGERPRINT=$(generate_fingerprint)
  STORED_FINGERPRINT=$(cat "$FINGERPRINT_FILE")

  if [ "$CURRENT_FINGERPRINT" != "$STORED_FINGERPRINT" ]; then
    echo "⚠️  package-lock.json changed! Re-installing dependencies..."
    npm clean-install
  else
    echo "✅ Dependencies are up to date."
    exit 0
  fi
fi

# Store the new fingerprint after installation
generate_fingerprint > "$FINGERPRINT_FILE"
echo "✅ Dependencies installed and fingerprint updated."