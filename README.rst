Micro Frontend base plugin for `Tutor <https://docs.tutor.overhang.io>`__
=========================================================================

This plugin makes it possible to easily add micro frontend (MFE) applications on top of an Open edX platform that runs with Tutor. To learn more about MFEs, please check the `official Open edX documentation <https://edx.readthedocs.io/projects/edx-developer-docs/en/latest/developers_guide/micro_frontends_in_open_edx.html>`__.

In addition, this plugin comes with a few MFEs which are enabled by default:

- `Account <https://github.com/openedx/frontend-app-account/>`__
- `Gradebook <https://github.com/openedx/frontend-app-gradebook/>`__
- `Learning <https://github.com/openedx/frontend-app-learning/>`__
- `Profile <https://github.com/openedx/frontend-app-profile/>`__
- `Course Authoring <https://github.com/opendx/frontend-app-course-authoring/>`__
- `Discussions <https://github.com/opendx/frontend-app-discussions/>`__
- `Authn <https://github.com/opendx/frontend-app-authn/>`__

Instructions for using each of these MFEs are given below.

Installation
------------

::

    pip install tutor-mfe

Usage
-----

To enable this plugin, run::

    tutor plugins enable mfe
    tutor local launch

When running the plugin in production, it is recommended that you set up a catch-all CNAME for subdomains at the DNS provider: see the `Configuring DNS Records <https://docs.tutor.overhang.io/install.html#configuring-dns-records>`__ section in the Tutor documentation for more details.  This way, the plugin will work out of the box with no additional configuration.  Which is to say, if your ``LMS_HOST`` is set to `myopenedx.com` the MFEs this plugin provides will be accessible under `apps.myopenedx.com` by default.

To check what the current value of `MFE_HOST` is actually set to, run the following::

    tutor config printvalue MFE_HOST


Account
~~~~~~~

.. image:: https://raw.githubusercontent.com/overhangio/tutor-mfe/master/screenshots/account.png
    :alt: Account MFE screenshot

An MFE to manage account-specific information for every LMS user. Each user's account page is available at ``http(s)://{{ MFE_HOST }}/account``. For instance, when running locally: https://apps.local.overhang.io/account.

Gradebook
~~~~~~~~~

.. image:: https://raw.githubusercontent.com/overhangio/tutor-mfe/master/screenshots/gradebook.png
    :alt: Gradebook MFE screenshot

This instructor-only MFE is for viewing individual and aggregated grade results for a course. To access this MFE, go to a course 🡒 🡒 Instructor tab 🡒 Student Admin 🡒 View gradebook. The URL should be: ``http(s)://{{ MFE_HOST }}/gradebook/{{ course ID }}``. When running locally, the gradebook of the demo course is available at: http://apps.local.overhang.io/gradebook/course-v1:edX+DemoX+Demo_Course

Learning
~~~~~~~~

.. image:: https://raw.githubusercontent.com/overhangio/tutor-mfe/master/screenshots/learning.png
    :alt: Learning MFE screenshot

The Learning MFE replaces the former courseware, which is the core part of the LMS where students follow courses.

Profile
~~~~~~~~~

.. image:: https://raw.githubusercontent.com/overhangio/tutor-mfe/master/screenshots/profile.png
    :alt: Profile MFE screenshot

Edit and display user-specific profile information. The profile page of every user is visible at ``http(s)://{{ MFE_HOST }}/profile/u/{{ username }}``. For instance, when running locally, the profile page of the "admin" user is: http://apps.local.overhang.io/profile/u/admin.

Course Authoring
~~~~~~~~~~~~~~~~

.. image:: https://raw.githubusercontent.com/overhangio/tutor-mfe/master/screenshots/course-authoring.png
    :alt: Course Authoring MFE screenshot

This MFE is meant for course authors and maintainers. For a given course, it exposes a "Pages & Resources" menu in Studio where one can enable or disable a variety of features, including, for example, the Wiki and Discussions.  Optionally, it allows authors to replace the legacy HTML, Video, and Problem authoring tools with experimental React-based versions, as well as exposing a new proctoring interface that can be enabled if the `edx-exams <https://github.com/edx/edx-exams>`_ service is available.

Discussions
~~~~~~~~~~~

.. image:: https://raw.githubusercontent.com/overhangio/tutor-mfe/master/screenshots/discussions.png
    :alt: Discussions MFE screenshot

The Discussions MFE updates the previous discussions UI with a new look and better features.

Authn
~~~~~~~~~

.. image:: https://raw.githubusercontent.com/overhangio/tutor-mfe/master/screenshots/authn.png
    :alt: Authn MFE screenshot

This is a micro-frontend application responsible for the login, registration and password reset functionality.

MFE management
--------------

Adding new MFEs
~~~~~~~~~~~~~~~

Other Tutor plugin developers can take advantage of this plugin to deploy their own MFEs. To declare a new MFE, a new configuration setting should be created with the "_MFE_APP" suffix. This configuration setting should include the name, repository, development port and production/development settings for the MFE. For example::

    config = {
        "defaults": {
            "MYMFE_MFE_APP": {
                "name": "mymfe",
                "repository": "https://github.com/myorg/mymfe",
                "port": 2001,
                "env": {
                    "production": {
                        "MY_CUSTOM_MFE_SETTING": "prod value"
                    },
                    "development": {
                        "MY_CUSTOM_MFE_SETTING": "dev value"
                    }
                }
            }
        }
    }

The MFE assets will then be bundled in the "mfe" Docker image and served at ``http(s)://{{ MFE_HOST }}/{{ MYMFE_MFE_APP["name"] }}``. Developers are free to add extra template patches to their plugins, as usual: for instance LMS setting patches to make sure that the LMS correctly connects to the MFEs.

Disabling individual MFEs
~~~~~~~~~~~~~~~~~~~~~~~~~

To disable an existing MFE, set its corresponding configuration setting to "null". For instance, to disable the MFEs that ship with this plugin::

    tutor config save --set MFE_ACCOUNT_MFE_APP=null
    tutor config save --set MFE_GRADEBOOK_MFE_APP=null
    tutor config save --set MFE_PROFILE_MFE_APP=null
    tutor config save --set MFE_COURSE_AUTHORING_MFE_APP=null
    tutor config save --set MFE_DISCUSSIONS_MFE_APP=null
    tutor config save --set MFE_AUTHN_MFE_APP=null

Adding custom translations to your MFEs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This plugin makes it possible to change existing and add new translation strings to MFEs. Here is how to do it:

1. Identify the ID of the string you would like to translate. For instance, the ID of the "Account Information" string in the account MFE is "account.settings.section.account.information" (see `source <https://github.com/edx/frontend-app-account/blob/1444831833cad4746b9ed14618a499b425ccc907/src/account-settings/AccountSettingsPage.messages.jsx#L34>`__).
2. Create a folder and i18n file corresponding to your MFE app and language in the Tutor root. This location of this file should be ``/path/to/tutor/env/plugins/mfe/build/mfe/i18n/<app name>/<language code>.json``. For instance, to add French ("fr") translation strings to the account MFE, run::

    cd "$(tutor config printroot)/env/plugins/mfe/build/mfe/i18n/"
    mkdir account
    touch account/fr.json

3. Add your entries to this file in JSON format, where the key is the string ID and the value is the actual string. For instance::

    {
      "account.settings.section.account.information": "Information du compte"
    }

4. Rebuild the MFE image and restart the MFE with::

    tutor images build mfe
    tutor local start -d

Your custom translation strings should now appear in your app.

Customising MFEs
~~~~~~~~~~~~~~~~

To change the MFEs logos from the default to your own logos, override the corresponding settings in the MFEs environment using patches `openedx-lms-production-settings` and `openedx-lms-development-settings`. For example, using the following plugin:
::

    from tutor import hooks

    hooks.Filters.ENV_PATCHES.add_item(
        (
            "openedx-lms-development-settings",
            """
    MFE_CONFIG["LOGO_URL"] = "<URL>/logo.svg"
    MFE_CONFIG["LOGO_TRADEMARK_URL"] = "<URL>/logo-trademark.svg"
    MFE_CONFIG["LOGO_WHITE_URL"] = "<URL>/logo-white.svg"
    MFE_CONFIG["FAVICON_URL"] = "<URL>/favicon.ico"
    """
        ),
        (
            "openedx-lms-production-settings",
            """
    MFE_CONFIG["LOGO_URL"] = "<URL>/logo.svg"
    MFE_CONFIG["LOGO_TRADEMARK_URL"] = "<URL>/logo-trademark.svg"
    MFE_CONFIG["LOGO_WHITE_URL"] = "<URL>/logo-white.svg"
    MFE_CONFIG["FAVICON_URL"] = "<URL>/favicon.ico"
    """
        ),
    )

To install custom components for the MFEs, such as the `header <https://github.com/openedx/frontend-component-header>`_ and `footer <https://github.com/openedx/frontend-component-footer>`_, override the components by adding a patch to ``mfe-dockerfile-post-npm-install`` in your plugin:
::

    from tutor import hooks

    hooks.Filters.ENV_PATCHES.add_item(
        (
            "mfe-dockerfile-post-npm-install",
            """
    # npm package
    RUN npm install '@edx/frontend-component-header@npm:@edx/frontend-component-header-edx@latest'
    # git repository
    RUN npm install '@edx/frontend-component-footer@git+https://github.com/edx/frontend-component-footer-edx.git'
    """
        )
    )

The same applies to installing a custom `brand <https://github.com/openedx/brand-openedx>`_ package:
::

    hooks.Filters.ENV_PATCHES.add_item(
        (
            "mfe-dockerfile-post-npm-install",
            """
    RUN npm install '@edx/brand@git+https://github.com/edx/brand-edx.org.git'
    """
        )
    )


Installing from a private npm registry
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In case you need to install components from a private NPM registry, you can append the ``--registry`` option to your install statement or add a ``npm config set`` command to the plugin.
In some cases, for example when using `GitLab's NPM package registry <https://docs.gitlab.com/ee/user/packages/npm_registry/>`_, you might also need to provide a token for your registry, which can be done with an additional ``npm config set`` command as well:
::

    from tutor import hooks

    hooks.Filters.ENV_PATCHES.add_item(
        (
            "mfe-dockerfile-post-npm-install",
            """
    RUN npm config set @foo:registry https://gitlab.example.com/api/v4/projects/<your_project_id>/packages/npm/
    RUN npm config set '//gitlab.example.com/api/v4/projects/<your_project_id>/packages/npm/:_authToken' '<your_token>'
    RUN npm install '@edx/frontend-component-header@npm:@foo/<your_frontend_component_header_name>@latest'
    """
        )
    )

MFE development
---------------

Tutor makes it possible to run any MFE in development mode. For instance, to run the "profile" MFE::

    tutor dev start profile

Then, access http://apps.local.overhang.io:1995/profile/u/YOURUSERNAME

You can also bind-mount your own fork of an MFE. For example::

    cd /path/to/frontend-app-profile
    npm install  # Ensure NPM requirements are installed into your fork.
    tutor dev start --mount=. profile

The changes you make to your fork will be automatically picked up and hot-reloaded by your development server.

This works for custom MFEs, as well. For example, if you added your own MFE named frontend-app-myapp, then you can bind-mount it like so::

    cd /path/to/frontend-app-myapp
    npm install
    tutor dev start --mount=. myapp

However, if you try to bind-mount an unknown MFE, you will see a Docker Compose error such as::

  ERROR: The Compose file is invalid because:
  Service myapp has neither an image nor a build context specified. At least one must be provided.

Please note that bind-mounting a fork is only available for development (``tutor dev ...``), since production MFEs are compiled and served out of a single container. If you want to use a fork of an MFE in production, then you will need to set the repository URL in ``$(tutor config printroot)/config.yml``::

    MFE_PROFILE_MFE_APP
        name: profile
        repository: "https://github.com/YOUR_FORK_ORGANIZATION/frontend-app-profile"
        port: 1995

and then rebuild the MFE container image with ``tutor images build mfe``.

Uninstall
---------

To disable this plugin run::

    tutor plugins disable mfe

You will also have to manually remove a few settings::

    # MFE account
    tutor local run lms ./manage.py lms waffle_delete --flags account.redirect_to_microfrontend

    # MFE profile
    tutor local run lms ./manage.py lms waffle_delete --flags learner_profile.redirect_to_microfrontend
    tutor local run lms ./manage.py lms waffle_delete --flags discussions.pages_and_resources_mfe
    tutor local run lms ./manage.py lms waffle_delete --flags new_core_editors.use_new_text_editor
    tutor local run lms ./manage.py lms waffle_delete --flags new_core_editors.use_new_video_editor
    tutor local run lms ./manage.py lms waffle_delete --flags new_core_editors.use_new_problem_editor
    tutor local run lms site-configuration unset ENABLE_PROFILE_MICROFRONTEND

    # MFE discussions
    tutor local run lms ./manage.py lms waffle_delete --flags discussions.enable_discussions_mfe
    tutor local run lms ./manage.py lms waffle_delete --flags discussions.enable_learners_tab_in_discussions_mfe
    tutor local run lms ./manage.py lms waffle_delete --flags discussions.enable_moderation_reason_codes
    tutor local run lms ./manage.py lms waffle_delete --flags discussions.enable_reported_content_email_notifications
    tutor local run lms ./manage.py lms waffle_delete --flags discussions.enable_learners_stats

Finally, restart the platform with::

    tutor local launch

Troubleshooting
---------------

This Tutor plugin is maintained by Adolfo Brandes from `tCRIL <https://openedx.org>`__. Community support is available from the official `Open edX forum <https://discuss.openedx.org>`__. Do you need help with this plugin? See the `troubleshooting <https://docs.tutor.overhang.io/troubleshooting.html>`__ section from the Tutor documentation.

License
-------

This software is licensed under the terms of the AGPLv3.
