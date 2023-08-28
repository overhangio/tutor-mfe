# Changelog

This file includes a history of past releases. Changes that were not yet added to a release are in the [changelog.d/](./changelog.d) folder.

<!--
⚠️ DO NOT ADD YOUR CHANGES TO THIS FILE! (unless you want to modify existing changelog entries in this file)
Changelog entries are managed by scriv. After you have made some changes to this plugin, create a changelog entry with:

    scriv create

Edit and commit the newly-created file in changelog.d.

If you need to create a new release, create a separate commit just for that. It is important to respect these
instructions, because git commits are used to generate release notes:
  - Modify the version number in `__about__.py`.
  - Collect changelog entries with `scriv collect`
  - The title of the commit should be the same as the new version: "vX.Y.Z".
-->

<!-- scriv-insert-here -->

<a id='changelog-16.1.1'></a>
## v16.1.1 (2023-08-28)

- [Bugfix] Add `INFO_EMAIL` and `PASSWORD_RESET_SUPPORT_LINK` missing variables defaults of `CONTACT_EMAIL` and `mailto:{{ CONTACT_EMAIL }}` respectfully. These two variables help build the "Forgot Password" screen. (by @misilot)
- [Bugfix] Corrected typo error in `PROFILE_MICROFRONTEND_URL` of development env settings. (by @kiran1415)

<a id='changelog-16.1.0'></a>
## v16.1.0 (2023-08-03)

- [Improvement] Allow patching the Dockerfile per MFE. (by @arbrandes)
- [Improvement] Invalidate build cache for individual MFEs if there were upstream changes. (by @arbrandes)
- [Improvement] Don't override `imagePullPolicy` in Kubernetes. This was only necessary in older releases. (by @regisb)
- [Improvement] Select GitHub refs API endpoint based on version suffix. (by @arbrandes)
- 💥[Improvement] Fix very high CPU and memory usage in development. We resolve this issue by running just a single container for all MFES, just like in production. To allow developers to test their changes in Tutor, we run `npm run start` only for those MFEs that have a manual bind-mount that was created with `tutor mounts add .../frontend-app-mymfe`. (by @regisb)
- [Bugfix] In development, fix link to profile in header. (by @regisb)

<a id='changelog-16.0.0'></a>
## v16.0.0 (2023-06-14)

- 💥[Feature] upgrade to Palm. With this new release, we make use of persistent bind-mounts to make it much easier to work on MFE forks. In addition, adding new MFEs is no longer done with `*_MFE_APP` settings, which was awkward, but with appropriate plugins. (by @regisb)
    - Add support for the ORA Grading MFE: The MFE is accessible by instructors in ORA exercises that have explicit staff grading steps.  The corresponding waffle flag is installed and enabled by default. (by @arbrandes)
    - Add support for the Communications MFE: The MFE is usable by instructors to send bulk email to learners in a course. The feature itself (the ability to send bulk email) pre-dates this MFE, and must be enabled as usual for the "Email" tab to become visible in the Instructor Dashboard.  The difference is that with this change, the tab will include a link to the MFE by default.
    - upgrade node to v18

<a id='changelog-15.0.7'></a>
## v15.0.7 (2023-05-26)

- [Bugfix] Fix un-clickable "account" menu item. (by @ghassanmas and @regisb)
- [Improvement] Add a scriv-compliant changelog. (by @regisb)

