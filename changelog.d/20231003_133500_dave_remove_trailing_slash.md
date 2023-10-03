
<!--
Create a changelog entry for every new user-facing change. Please respect the following instructions:
- Indicate breaking changes by prepending an explosion 💥 character.
- Prefix your changes with either [Bugfix], [Improvement], [Feature], [Security], [Deprecation].
- You may optionally append "(by @<author>)" at the end of the line, where "<author>" is either one (just one)
of your GitHub username, real name or affiliated organization. These affiliations will be displayed in
the release notes for every release.
-->

- [Bugfix] Remove the trailing slash from auto-generated PUBLIC_PATH env vars for MFEs in order to be consistent with LMS/Studio config, and so that we don't have to strip it off on the JavaScript side after the React Router 6 upgrade. (by @ormsbee)
