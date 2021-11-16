Micro Frontend base plugin for `Tutor <https://docs.tutor.overhang.io>`__
=========================================================================

This plugin makes it possible to easily add micro frontend (MFE) applications on top of an Open edX platform that runs with Tutor. To learn more about MFEs, please check the `official Open edX documentation <https://edx.readthedocs.io/projects/edx-developer-docs/en/latest/developers_guide/micro_frontends_in_open_edx.html>`__.

In addition, this plugin comes with a few MFEs which are enabled by default:

- `Account <https://github.com/edx/frontend-app-account/>`__
- `Gradebook <https://github.com/edx/frontend-app-gradebook/>`__
- `Learning <https://github.com/edx/frontend-app-learning/>`__
- `Profile <https://github.com/edx/frontend-app-profile/>`__

Instructions for using each of these MFEs are given below.

Installation
------------

::

    pip install tutor-mfe

Usage
-----

::

    tutor plugins enable mfe
    tutor local quickstart

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
      "account.settings.section.account.information": "Information du compte POUAC"
    }

4. Rebuild the MFE image and restart the MFE with::

    tutor images build mfe
    tutor local start -d

Your custom translation strings should now appear in your app.

Customise MFEs Logos
~~~~~~~~~~~~~~~~~~~~~~~~~

To change the MFEs logos from the default to your own logos, override the corresponding settings in the MFEs environment using patches `mfe-env-production` and `mfe-env-development`. For example, using the following plugin:
::

    name: mfe_branding_plugin
    version: 0.1.0
    patches:
    mfe-env-development: |
        LOGO_URL=<URL>/logo.svg
        LOGO_TRADEMARK_URL=<URL>/logo-trademark.svg
        LOGO_WHITE_URL=<URL>/logo-white.svg
        FAVICON_URL=<URL>/favicon.ico
    mfe-env-production: |
        LOGO_URL=<URL>/logo.svg
        LOGO_TRADEMARK_URL=<URL>/logo-trademark.svg
        LOGO_WHITE_URL=<URL>/logo-white.svg
        FAVICON_URL=<URL>/favicon.ico


Running MFEs on Kubernetes
--------------------------

The MFE plugin works a bit differently than other Tutor plugins. MFEs are static bundles of js/html/css code that must be re-generated after every change to their configuration. In practice, this means that the "mfe" Docker image should be re-built and re-deployed every time we run ``tutor config save``. This happens transparently when running Open edX locally (with ``tutor local``). But when running on Kubernetes, you need to re-build the "mfe" image manually and push it to a remote registry. In effect, you must run::

    tutor config save --set MFE_DOCKER_IMAGE=docker.io/yourusername/openedx-mfe:latest
    tutor images build mfe
    tutor images push mfe
    tutor k8s start

We consider that this situation is less than ideal. An improvement would be to self-host a Docker registry and an image-building pipeline on Kubernetes. If you are interested in such a solution, please let your voice be heard on the `Tutor community forums <https://discuss.overhang.io>`__.

MFE development
---------------

Tutor makes it possible to run any MFE in development mode. For instance, to run the "profile" MFE::

    tutor dev runserver profile

Then, access http://apps.local.overhang.io:1995/profile/u/YOURUSERNAME

To run your own fork of an MFE, start by copying the MFE repo on the host::

    tutor dev bindmount profile /openedx/app

Then, run a development server that bind-mounts the repo::

    tutor dev runserver --volume=/openedx/app profile

The changes you make to ``$(tutor config printroot)/volumes/app/`` will be automatically picked up and hot-reloaded by your development server.

Uninstall
---------

To disable this plugin run::

    tutor plugins disable mfe

You will also have to manually remove a few waffle flags::

    tutor local run lms ./manage.py lms waffle_delete --flags account.redirect_to_microfrontend
    tutor local run lms ./manage.py lms waffle_delete --flags learner_profile.redirect_to_microfrontend
    tutor local run lms site-configuration unset ENABLE_PROFILE_MICROFRONTEND

Finally, restart the platform with::

    tutor local quickstart

License
-------

This software is licensed under the terms of the AGPLv3.
