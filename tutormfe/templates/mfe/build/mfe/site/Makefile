TURBO = TURBO_TELEMETRY_DISABLED=1 turbo --dangerously-disable-package-manager-check

.PHONY: bin-link build-packages clean-packages clean dev-packages

# NPM doesn't bin-link workspace packages during install, so it must be done manually.
bin-link:
	[ -f packages/frontend-base/package.json ] && npm rebuild --ignore-scripts @openedx/frontend-base || true

build-packages:
	$(TURBO) run build
	$(MAKE) bin-link

clean-packages:
	$(TURBO) run clean

dev-packages:
	# Remove nested node_modules from bind-mounted packages to avoid
	# duplicate dependency issues (e.g., two React instances).
	find packages -maxdepth 2 -name node_modules -type d -exec rm -rf {} + 2>/dev/null || true
	# Re-establish workspace symlinks for any bind-mounted packages.
	npm install
	# Clean stale build artifacts from bind-mounted packages.
	$(MAKE) clean-packages
	$(TURBO) run watch:build dev:site

dev-site: bin-link
	npm run dev

pull_translations:
	npm run translations:pull

clean:
	rm -rf dist
