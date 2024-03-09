Micro Frontend base plugin for `Tutor <https://docs.tutor.edly.io>`__
=========================================================================

This plugin makes it possible to easily add micro frontend (MFE) applications on top of an Open edX platform that runs with Tutor. To learn more about MFEs, please check the `official Open edX documentation <https://edx.readthedocs.io/projects/edx-developer-docs/en/latest/developers_guide/micro_frontends_in_open_edx.html>`__.

In addition, this plugin comes with a few MFEs which are enabled by default:

- `Authn <https://github.com/openedx/frontend-app-authn/>`__
- `Account <https://github.com/openedx/frontend-app-account/>`__
- `Communications <https://github.com/openedx/frontend-app-communications/>`__
- `Course Authoring <https://github.com/openedx/frontend-app-course-authoring/>`__
- `Discussions <https://github.com/openedx/frontend-app-discussions/>`__
- `Gradebook <https://github.com/openedx/frontend-app-gradebook/>`__
- `Learner Dashboard <https://github.com/openedx/frontend-app-learner-dashboard/>`__
- `Learning <https://github.com/openedx/frontend-app-learning/>`__
- `ORA Grading <https://github.com/openedx/frontend-app-ora-grading/>`__
- `Profile <https://github.com/openedx/frontend-app-profile/>`__

Instructions for using each of these MFEs are given below.

Installation
------------

::

    tutor plugins install mfe

Usage
-----

To enable this plugin, run::

    tutor plugins enable mfe
    tutor local launch

When running the plugin in production, it is recommended that you set up a catch-all CNAME for subdomains at the DNS provider: see the `Configuring DNS Records <https://docs.tutor.edly.io/install.html#configuring-dns-records>`__ section in the Tutor documentation for more details.  This way, the plugin will work out of the box with no additional configuration.  Which is to say, if your ``LMS_HOST`` is set to `myopenedx.com` the MFEs this plugin provides will be accessible under `apps.myopenedx.com` by default.

To check what the current value of `MFE_HOST` is actually set to, run::

    tutor config printvalue MFE_HOST

Authn
~~~~~~~~~

.. image:: https://raw.githubusercontent.com/overhangio/tutor-mfe/master/screenshots/authn.png
    :alt: Authn MFE screenshot

This is a micro-frontend application responsible for the login, registration and password reset functionality.

Account
~~~~~~~

.. image:: https://raw.githubusercontent.com/overhangio/tutor-mfe/master/screenshots/account.png
    :alt: Account MFE screenshot

An MFE to manage account-specific information for every LMS user. Each user's account page is available at ``http(s)://{{ MFE_HOST }}/account``. For instance, when running locally: https://apps.local.edly.io/account.

Communications
~~~~~~~~~~~~~~

.. image:: https://raw.githubusercontent.com/overhangio/tutor-mfe/master/screenshots/communications.png
    :alt: Communications MFE screenshot

The Communications micro-frontend exposes an interface for course teams to communicate with learners.  It achieves this by allowing instructors to send out emails in bulk, either by scheduling them or on demand.

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

Gradebook
~~~~~~~~~

.. image:: https://raw.githubusercontent.com/overhangio/tutor-mfe/master/screenshots/gradebook.png
    :alt: Gradebook MFE screenshot

This instructor-only MFE is for viewing individual and aggregated grade results for a course. To access this MFE, go to a course → Instructor tab → Student Admin → View gradebook. The URL should be: ``http(s)://{{ MFE_HOST }}/gradebook/{{ course ID }}``. When running locally, the gradebook of the demo course is available at: http://apps.local.edly.io/gradebook/course-v1:edX+DemoX+Demo_Course

Learner Dashboard
~~~~~~~~~~~~~~~~~

.. image:: https://raw.githubusercontent.com/overhangio/tutor-mfe/master/screenshots/learner-dashboard.png
    :alt: Learner Dashboard MFE screenshot

The Learner Dashboard MFE provides a clean and functional interface to allow learners to view all of their open enrollments, as well as take relevant actions on those enrollments.

Learning
~~~~~~~~

.. image:: https://raw.githubusercontent.com/overhangio/tutor-mfe/master/screenshots/learning.png
    :alt: Learning MFE screenshot

The Learning MFE replaces the former courseware, which is the core part of the LMS where students follow courses.

ORA Grading
~~~~~~~~~~~

.. image:: https://raw.githubusercontent.com/overhangio/tutor-mfe/master/screenshots/ora-grading.png
    :alt: ORA Grading MFE screenshot

When enabled, Open Response Assessments ("ORA") that have a staff grading step will link to this new MFE, either when clicking "Grade Available Responses" from the exercise itself, or via a link in the Instructor Dashboard.  It is meant to streamline the grading process with better previews of submitted content.

Profile
~~~~~~~~~

.. image:: https://raw.githubusercontent.com/overhangio/tutor-mfe/master/screenshots/profile.png
    :alt: Profile MFE screenshot

Edit and display user-specific profile information. The profile page of every user is visible at ``http(s)://{{ MFE_HOST }}/profile/u/{{ username }}``. For instance, when running locally, the profile page of the "admin" user is: http://apps.local.edly.io/profile/u/admin.


MFE management
--------------

Adding new MFEs
~~~~~~~~~~~~~~~

⚠️ **Warnings**

- As of Tutor v16 (Palm release) it is no longer possible to add new MFEs by creating ``*_MFE_APP`` settings. Instead, users must implement the approach described below.
- As of Tutor v17 (Quince release) you must make sure that the git URL of your MFE repository ends with ``.git``. Otherwise the plugin build will fail.
- As of Tutor v18 (Redwood release) all MFEs must provide a ``make pull_translations`` command. Otherwise the plugin build will fail. Providing an empty command is enough to bypass this requirement. See the `Custom translations section <#mfe-custom-translations>`_ for more information.

Other MFE developers can take advantage of this plugin to deploy their own MFEs. To declare a new MFE, create a Tutor plugin and add your MFE configuration to the ``tutormfe.hooks.MFE_APPS`` filter. This configuration should include the name, git repository (and optionally: git branch or tag) and development port. For example::

    from tutormfe.hooks import MFE_APPS

    @MFE_APPS.add()
    def _add_my_mfe(mfes):
        mfes["mymfe"] = {
            "repository": "https://github.com/myorg/mymfe.git",
            "port": 2001,
            "version": "me/my-custom-branch-or-tag", # optional, will default to the Open edX current tag.
        }
        return mfes

The MFE assets will then be bundled in the "mfe" Docker image whenever it is rebuilt with ``tutor images build mfe``.

Assets will be served at ``http(s)://{{ MFE_HOST }}/mymfe``. Developers are free to add extra template patches to their plugins, as usual: for instance LMS setting patches to make sure that the LMS correctly connects to the MFEs.

Disabling individual MFEs
~~~~~~~~~~~~~~~~~~~~~~~~~

To disable an existing MFE, remove the corresponding entry from the ``MFE_APPS`` filter. For instance, to disable some of the MFEs that ship with this plugin::


    @MFE_APPS.add()
    def _remove_some_my_mfe(mfes):
        mfes.pop("account")
        mfes.pop("profile")
        return mfes

Using custom translations to your MFEs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _mfe-custom-translations:

During docker image build, this plugin runs ``make pull_translations`` for each Micro-frontend. This
program is used in the ``Dockerfile`` to pull translations from the `openedx/openedx-translations repository <https://github.com/openedx/openedx-translations>`_ via `openedx-atlas <https://github.com/openedx/openedx-atlas>`_.

The ``make pull_translations`` command passes the ``ATLAS_OPTIONS`` environment variable to the ``atlas pull`` command. This allows specifying a custom repository or branch to pull translations from.

Translations in the MFE plugin as well as other Tutor plugins can be customized with the following configuration
variables:

- ``ATLAS_REVISION`` (default: ``"main"`` on nightly and ``"{{ OPENEDX_COMMON_VERSION }}"`` if a named release is used)
- ``ATLAS_REPOSITORY`` (default: ``"openedx/openedx-translations"``).
- ``ATLAS_OPTIONS`` (default: ``""``) Pass additional arguments to ``atlas pull``. Refer to the `atlas documentations <https://github.com/openedx/openedx-atlas>`_ for more information.

The
`Getting and customizing Translations <https://docs.tutor.edly.io/configuration.html#getting-and-customizing-translations>`_
section in the Tutor configuration documentation explains how to do this.

Customising MFEs
~~~~~~~~~~~~~~~~

.. _mfe-lms-settings:

To change the MFEs logos from the default to your own logos, override the corresponding settings in the MFEs environment using patches `mfe-lms-production-settings` and `mfe-lms-development-settings`. For example, using the following plugin:
::

    from tutor import hooks

    hooks.Filters.ENV_PATCHES.add_items(
        [
            (
                "mfe-lms-development-settings",
                """
        MFE_CONFIG["LOGO_URL"] = "<URL>/logo.svg"
        MFE_CONFIG["LOGO_TRADEMARK_URL"] = "<URL>/logo-trademark.svg"
        MFE_CONFIG["LOGO_WHITE_URL"] = "<URL>/logo-white.svg"
        MFE_CONFIG["FAVICON_URL"] = "<URL>/favicon.ico"
        """
            ),
            (
                "mfe-lms-production-settings",
                """
        MFE_CONFIG["LOGO_URL"] = "<URL>/logo.svg"
        MFE_CONFIG["LOGO_TRADEMARK_URL"] = "<URL>/logo-trademark.svg"
        MFE_CONFIG["LOGO_WHITE_URL"] = "<URL>/logo-white.svg"
        MFE_CONFIG["FAVICON_URL"] = "<URL>/favicon.ico"
        """
            ),
        ]
    )

If patches are the same in development and production, they can be replaced by a single `mfe-lms-common-settings` patch.

.. _mfe-docker-post-npm-install:

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

In both cases above, the ``npm`` commands affect every MFE being built.  If you want have different commands apply to different MFEs, you can add one or more patches to ``mfe-dockerfile-post-npm-install-*`` instead.  For instance, you could install one particular version of the header to the Learning MFE by patching ``mfe-dockerfile-post-npm-install-learning``, and another one to the ORA Grading MFE by patching ``mfe-dockerfile-post-npm-install-ora-grading``::

    hooks.Filters.ENV_PATCHES.add_items(
        [
            (
                "mfe-dockerfile-post-npm-install-learning",
                """
        RUN npm install '@edx/frontend-component-header@git+https://github.com/your-repo/frontend-component-header.git#your-branch'
        """
            ),
            (
                "mfe-dockerfile-post-npm-install-ora-grading",
                """
        RUN npm install '@edx/frontend-component-header@git+https://github.com/your-repo/frontend-component-header.git#your-other-branch'
        """
            ),
        ]
    )

.. _mfe-docker-pre-npm-build:

In case you need to run additional instructions just before the build step you can use the ``mfe-dockerfile-pre-npm-build`` or ``mfe-dockerfile-pre-npm-build-*`` patches. For example, you may want to override existing env variables or define new ones.
::

    from tutor import hooks

    hooks.Filters.ENV_PATCHES.add_items(
        [
            (
                "mfe-dockerfile-pre-npm-build",
                """
    ENV ENABLE_NEW_RELIC=true
    ENV NEW_RELIC_ACCOUNT_ID="111111"
    ENV NEW_RELIC_AGENT_ID="2222222222"
    ENV NEW_RELIC_TRUST_KEY="333333"
    ENV NEW_RELIC_LICENSE_KEY="4444444444"
    ENV NEW_RELIC_APP_ID="5555555555"
    """
            ),
            # Only for the learning MFE
            (
                "mfe-dockerfile-pre-npm-build-learning",
                """ENV CUSTOM_VAR="custom-value"
                """
            ),
        ]
    )

You can find more patches in the `patch catalog <#template-patch-catalog>`_ below.

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

Then, access http://apps.local.edly.io:1995/profile/u/YOURUSERNAME

You can also bind-mount your own fork of an MFE. For example::

    tutor mounts add /path/to/frontend-app-profile
    tutor dev launch

.. note::

  The name of the bind-mount folder needs to match the name of the repository word-for-word. If you've forked an MFE repository with a custom name, be sure to change the name back to ensure the bind-mount works properly.

With this change, the "profile-dev" image will be automatically re-built during ``launch``. Your host repository will then be bind-mounted at runtime in the "profile" container. This means that changes you make to the host repository will be automatically picked up and hot-reloaded by your development server.

This works for custom MFEs, as well. For example, if you added your own MFE named frontend-app-myapp, then you can bind-mount it like so::

    tutor mounts add /path/to/frontend-app-myapp

Similarly, in production, the "mfe" Docker image will be rebuilt automatically during ``tutor local launch``.

.. note::

  Docker tries to run as many build processes in parallel as possible, but this can cause failures in the MFE image build.  If you're running into OOM issues, RAM starvation, or network failures during NPM installs, try the following before restarting::

    cat >buildkitd.toml <<EOF
    [worker.oci]
      max-parallelism = 1
    EOF
    docker buildx create --use --name=singlecpu --config=./buildkitd.toml

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

    # MFE ora-grading
    tutor local run lms ./manage.py lms waffle_delete --flags openresponseassessment.enhanced_staff_grader

Finally, restart the platform with::

    tutor local launch


Template patch catalog
----------------------

This is the list of all patches used across tutor-mfe (outside of any plugin). Alternatively, you can search for patches in tutor-mfe templates by grepping the source code::
    
    git clone https://github.com/overhangio/tutor-mfe
    cd tutor-mfe
    git grep "{{ patch" -- tutormfe/templates

mfe-lms-development-settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Python-formatted LMS settings in development. Values defined here override the values from `mfe-lms-common-settings <#mfe-lms-common-settings>`_ or `mfe-lms-production-settings <#mfe-lms-production-settings>`_. For an example on the usage of this patch, check out `this section <#mfe-lms-settings>`_.

File changed: ``apps/openedx/settings/lms/development.py``

mfe-lms-production-settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Python-formatted LMS settings in production. Values defined here override the values from `mfe-lms-common-settings <#mfe-lms-common-settings>`_. For an example on the usage of this patch, check out `this section <#mfe-lms-settings>`_.

File changed: ``apps/openedx/settings/lms/production.py``

mfe-lms-common-settings
~~~~~~~~~~~~~~~~~~~~~~~
Python-formatted LMS settings used both in production and development.

File changed: ``apps/openedx/settings/partials/common_lms.py``

mfe-webpack-dev-config
~~~~~~~~~~~~~~~~~~~~~~
Add any configurations at the end of the development webpack config file in Javascript format.

File changed: ``tutormfe/templates/mfe/apps/mfe/webpack.dev-tutor.config.js``

mfe-dockerfile-pre-npm-install
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Add any instructions for before the npm install is initiated.

File changed: ``tutormfe/templates/mfe/build/mfe/Dockerfile``

mfe-dockerfile-pre-npm-install-{}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Add any instructions for before the npm install is initiated for a specific MFE. Add the exact MFE name at the end to only change instructions for that MFE.

Example: ``mfe-dockerfile-pre-npm-install-learning`` will only apply any instructions specified for the learning MFE.

File changed: ``tutormfe/templates/mfe/build/mfe/Dockerfile``

mfe-dockerfile-production-final
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Add any instructions in the final layer. Useful for overriding the CMD or ENTRYPOINT.

File changed: ``tutormfe/templates/mfe/build/mfe/Dockerfile``

mfe-dockerfile-post-npm-install
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Add any instructions for after the npm install has completed. This will apply the instructions to every MFE. For an example on the usage of this patch, check out `here <#mfe-docker-post-npm-install>`_.

File changed: ``tutormfe/templates/mfe/build/mfe/Dockerfile``

mfe-dockerfile-post-npm-install-{}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Add any instructions for after the npm install has completed for a specific MFE. Add the exact MFE name at the end to only change instructions for that MFE. For an example on the usage of this patch, check out `here <#mfe-docker-post-npm-install>`_.

Example: ``mfe-dockerfile-post-npm-install-authn`` will only apply any instructions specified for the authn MFE.

File changed: ``tutormfe/templates/mfe/build/mfe/Dockerfile``

mfe-dockerfile-pre-npm-build
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Add any instructions for before the build step initializes. This will apply the instructions to every MFE. For an example on the usage of this patch, see `over here <#mfe-docker-pre-npm-build>`_.

File changed: ``tutormfe/templates/mfe/build/mfe/Dockerfile``

mfe-dockerfile-pre-npm-build-{}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Add any instructions for before the build step initializes for a specific MFE. Add the exact MFE name at the end to only change instructions for that MFE. For an example on the usage of this patch, see `over here <#mfe-docker-pre-npm-build>`_.

Example: ``mfe-dockerfile-post-npm-build-learning`` will only apply any instructions specified for the learning MFE.

File changed: ``tutormfe/templates/mfe/build/mfe/Dockerfile``

mfe-dockerfile-post-npm-build
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Add any instructions for after the build step has completed. This will apply the instructions to every MFE.

File changed: ``tutormfe/templates/mfe/build/mfe/Dockerfile``

mfe-dockerfile-post-npm-build-{}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Add any instructions for after the build step has completed for a specific MFE. Add the exact MFE name at the end to only change instructions for that MFE.

Example: ``mfe-dockerfile-post-npm-build-learning`` will only apply any instructions specified for the learning MFE.

File changed: ``tutormfe/templates/mfe/build/mfe/Dockerfile``

mfe-caddyfile
~~~~~~~~~~~~~
Add any configurations for the mfe-caddyfile.

File changed: ``tutormfe/templates/mfe/apps/mfe/Caddyfile``


Troubleshooting
---------------

This Tutor plugin is maintained by Adolfo Brandes from `tCRIL <https://openedx.org>`__. Community support is available from the official `Open edX forum <https://discuss.openedx.org>`__. Do you need help with this plugin? See the `troubleshooting <https://docs.tutor.edly.io/troubleshooting.html>`__ section from the Tutor documentation.

License
-------

This software is licensed under the terms of the `GNU Affero General Public License (AGPL) <https://github.com/overhangio/tutor-mfe/blob/master/LICENSE.txt>`_.
