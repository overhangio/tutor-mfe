#!/bin/bash
# TODO(legacy-mfe-removal)
# Install node_modules in a bind-mounted MFE repository before the dev server starts.
# The node_modules from the image are hidden by the bind-mount, and the host repository
# usually doesn't have its own, which results in "fedx-scripts: not found" errors.
set -e

# Only explicit mounts of sub-directories were added: the image node_modules are still visible
if ! mountpoint -q /openedx/app; then
    exit 0
fi

FINGERPRINT_FILE="node_modules/.tutor-package-lock-sha1"

# Skip the install when node_modules were installed from the current package-lock.json
fingerprint="$(sha1sum package-lock.json | cut -d ' ' -f 1)"
if [ -f "$FINGERPRINT_FILE" ] && [ "$(cat "$FINGERPRINT_FILE")" = "$fingerprint" ]; then
    echo "node_modules are up to date with package-lock.json"
    exit 0
fi

echo "node_modules are missing or out of date with package-lock.json, installing..."
npm clean-install --no-audit --no-fund --registry={{ NPM_REGISTRY }}
echo "$fingerprint" > "$FINGERPRINT_FILE"

# The container runs as root: give ownership of node_modules back to the owner of the
# host repository, such that it can still be modified or removed outside of the container.
chown -R "$(stat -c '%u:%g' .)" node_modules
