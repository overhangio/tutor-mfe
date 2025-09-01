Micro Frontend base plugin for `Tutor <https://docs.tutor.edly.io>`__
=========================================================================

This plugin makes it possible to easily add micro frontend (MFE) applications on top of an Open edX platform that runs with Tutor. To learn more about MFEs, please check the `official Open edX documentation <https://openedx.github.io/frontend-platform/>`__.

In addition, this plugin comes with a few MFEs which are enabled by default:

- `Authn <https://github.com/openedx/frontend-app-authn/>`__
- `Authoring <https://github.com/openedx/frontend-app-authoring/>`__
- `Account <https://github.com/openedx/frontend-app-account/>`__
- `Communications <https://github.com/openedx/frontend-app-communications/>`__
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

Account
~~~~~~~

.. image:: https://raw.githubusercontent.com/overhangio/tutor-mfe/release/media/account.png
    :alt: Account MFE screenshot

An MFE to manage account-specific information for every LMS user. Each user's account page is available at ``http(s)://{{ MFE_HOST }}/account``. For instance, when running locally: https://apps.local.openedx.io/account.

Authn
~~~~~

.. image:: https://raw.githubusercontent.com/overhangio/tutor-mfe/release/media/authn.png
    :alt: Authn MFE screenshot

This is a micro-frontend application responsible for the login, registration and password reset functionality.

Authoring
~~~~~~~~~

.. image:: https://raw.githubusercontent.com/overhangio/tutor-mfe/release/media/authoring.png
    :alt: Course Authoring MFE screenshot

This MFE is meant for course authors and maintainers. For a given course, it exposes a "Pages & Resources" menu in Studio where one can enable or disable a variety of features, including, for example, the Wiki and Discussions.  Optionally, it allows authors to replace the legacy HTML, Video, and Problem authoring tools with experimental React-based versions, as well as exposing a new proctoring interface that can be enabled if the `edx-exams <https://github.com/edx/edx-exams>`_ service is available.


Communications
~~~~~~~~~~~~~~

.. image:: https://raw.githubusercontent.com/overhangio/tutor-mfe/release/media/communications.png
    :alt: Communications MFE screenshot

The Communications micro-frontend exposes an interface for course teams to communicate with learners.  It achieves this by allowing instructors to send out emails in bulk, either by scheduling them or on demand.

Discussions
~~~~~~~~~~~

.. image:: https://raw.githubusercontent.com/overhangio/tutor-mfe/release/media/discussions.png
    :alt: Discussions MFE screenshot

The Discussions MFE updates the previous discussions UI with a new look and better features.

Gradebook
~~~~~~~~~

.. image:: https://raw.githubusercontent.com/overhangio/tutor-mfe/release/media/gradebook.png
    :alt: Gradebook MFE screenshot

This instructor-only MFE is for viewing individual and aggregated grade results for a course. To access this MFE, go to a course → Instructor tab → Student Admin → View gradebook. The URL should be: ``http(s)://{{ MFE_HOST }}/gradebook/{{ course ID }}``. When running locally, the gradebook of the demo course is available at: http://apps.local.openedx.io/gradebook/course-v1:edX+DemoX+Demo_Course

Learner Dashboard
~~~~~~~~~~~~~~~~~

.. image:: https://raw.githubusercontent.com/overhangio/tutor-mfe/release/media/learner-dashboard.png
    :alt: Learner Dashboard MFE screenshot

The Learner Dashboard MFE provides a clean and functional interface to allow learners to view all of their open enrollments, as well as take relevant actions on those enrollments.

Learning
~~~~~~~~

.. image:: https://raw.githubusercontent.com/overhangio/tutor-mfe/release/media/learning.png
    :alt: Learning MFE screenshot

The Learning MFE replaces the former courseware, which is the core part of the LMS where students follow courses.

ORA Grading
~~~~~~~~~~~

.. image:: https://raw.githubusercontent.com/overhangio/tutor-mfe/release/media/ora-grading.png
    :alt: ORA Grading MFE screenshot

When enabled, Open Response Assessments ("ORA") that have a staff grading step will link to this new MFE, either when clicking "Grade Available Responses" from the exercise itself, or via a link in the Instructor Dashboard.  It is meant to streamline the grading process with better previews of submitted content.

Profile
~~~~~~~

.. image:: https://raw.githubusercontent.com/overhangio/tutor-mfe/release/media/profile.png
    :alt: Profile MFE screenshot

Edit and display user-specific profile information. The profile page of every user is visible at ``http(s)://{{ MFE_HOST }}/profile/u/{{ username }}``. For instance, when running locally, the profile page of the "admin" user is: http://apps.local.openedx.io/profile/u/admin.


MFE management
--------------

Adding new MFEs
~~~~~~~~~~~~~~~

⚠️ **Warnings**

- As of Tutor v16 (Palm release) it is no longer possible to add new MFEs by creating ``*_MFE_APP`` settings. Instead, users must implement the approach described below.
- As of Tutor v17 (Quince release) you must make sure that the git URL of your MFE repository ends with ``.git``. Otherwise the plugin build will fail.
- As of Tutor v18 (Redwood release) all MFEs must provide a ``make pull_translations`` command. Otherwise the plugin build will fail. Providing an empty command is enough to bypass this requirement. See the `Custom translations section <#mfe-custom-translations>`_ for more information.

Other MFE developers can take advantage of this plugin to deploy their own MFEs. To declare a new MFE, create a Tutor plugin and add your MFE configuration to the ``tutormfe.hooks.MFE_APPS`` filter. This configuration should include the name, git repository (and optionally: git branch or tag) and development port. For example:

.. code-block:: python

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

To disable an existing MFE, remove the corresponding entry from the ``MFE_APPS`` filter. For instance, to disable some of the MFEs that ship with this plugin:

.. code-block:: python

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

- ``ATLAS_REVISION`` (default: ``"main"`` on tutor Main branch and ``"{{ OPENEDX_COMMON_VERSION }}"`` if a named release is used)
- ``ATLAS_REPOSITORY`` (default: ``"openedx/openedx-translations"``).
- ``ATLAS_OPTIONS`` (default: ``""``) Pass additional arguments to ``atlas pull``. Refer to the `atlas documentations <https://github.com/openedx/openedx-atlas>`_ for more information.

The
`Getting and customizing Translations <https://docs.tutor.edly.io/configuration.html#getting-and-customizing-translations>`_
section in the Tutor configuration documentation explains how to do this.

Customising MFEs
~~~~~~~~~~~~~~~~

.. _mfe-lms-settings:

To change the MFEs logos from the default to your own logos, override the corresponding settings in the MFEs environment using patches `mfe-lms-production-settings` and `mfe-lms-development-settings`. For example, using the following plugin:

.. code-block:: python

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

If patches are the same in development and production, they can be replaced by a single ``mfe-lms-common-settings`` patch.

.. _mfe-docker-post-npm-install:

To install custom components for the MFEs, such as the `header <https://github.com/openedx/frontend-component-header>`_ and `footer <https://github.com/openedx/frontend-component-footer>`_, override the components by adding a patch to ``mfe-dockerfile-post-npm-install`` in your plugin:

.. code-block:: python

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

.. code-block:: python

    hooks.Filters.ENV_PATCHES.add_item(
        (
            "mfe-dockerfile-post-npm-install",
            """
    RUN npm install '@edx/brand@git+https://github.com/edx/brand-edx.org.git'
    """
        )
    )

In both cases above, the ``npm`` commands affect every MFE being built.  If you want have different commands apply to different MFEs, you can add one or more patches to ``mfe-dockerfile-post-npm-install-*`` instead.  For instance, you could install one particular version of the header to the Learning MFE by patching ``mfe-dockerfile-post-npm-install-learning``, and another one to the ORA Grading MFE by patching ``mfe-dockerfile-post-npm-install-ora-grading``:

.. code-block:: python

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

.. code-block:: python

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

Using Frontend Plugin Slots
~~~~~~~~~~~~~~~~~~~~~~~~~~~

It's possible to take advantage of this plugin's hooks to configure frontend plugin slots. Let's say you want to replace the entire footer with a simple message. Where before you might have had to fork ``frontend-component-footer``, the following is all that's currently needed:

.. code-block:: python

    from tutormfe.hooks import PLUGIN_SLOTS

    PLUGIN_SLOTS.add_items([
        # Hide the default footer
        (
            "all",
            "footer_slot",
            """
            {
              op: PLUGIN_OPERATIONS.Hide,
              widgetId: 'default_contents',
            }"""
        ),
        # Insert a custom footer
        (
            "all",
            "footer_slot",
            """
            {
              op: PLUGIN_OPERATIONS.Insert,
              widget: {
                id: 'custom_footer',
                type: DIRECT_PLUGIN,
                RenderWidget: () => (
                  <h1>This is the footer.</h1>
                ),
              },
            }"""
        )
    ])

Let's take a closer look at what's happening here.  To begin with, we're using tutormfe's own ``PLUGIN_SLOTS`` filter.  It's a regular Tutor filter, but you won't find it in the main ``tutor`` package:

.. code-block:: python

    from tutormfe.hooks import PLUGIN_SLOTS

Next up, we're adding actual slot configuration, starting by hiding the default footer.  The first parameter in a filter item specifies which MFE to apply the slot configuration to; for example: ``"learner-dashboard"``, or ``"learning"``. We're using ``"all"`` here, which is a special case: it means the slot configuration should be applied to all MFEs that actually have that slot.  (If a particular MFE doesn't have the slot, it will just ignore its configuration.)

The second parameter, ``"footer_slot"``, is the name of the slot as defined in the code of the MFE itself.

.. code-block:: python

    PLUGIN_SLOTS.add_items([
        # Hide the default footer
        (
            "all",
            "footer_slot",
            """
            {
              op: PLUGIN_OPERATIONS.Hide,
              widgetId: 'default_contents',
            }"""
        ),

The last parameter to ``add_item()`` is a big string with the actual slot configuration, which will be interpreted as JSX. What we're doing there is hiding the default contents of the footer with a ``PLUGIN_OPERATIONS.Hide``. (You can refer to the `frontend-plugin-framework README <https://github.com/openedx/frontend-plugin-framework/#>`_ for a full description of the possible plugin types and operations.) And the ``default_contents`` widget ID we're targetting always refers to what's in an unconfigured slot by default.

In the second filter item, we once again target the ``"footer_slot"`` on ``"all"`` MFEs. This time, we use ``PLUGIN_OPERATIONS.Insert`` to add our custom JSX component, comprised of a simple ``<h1>`` message we're defining in an anonymous function. We give it a widgetID of ``custom_footer``:

.. code-block:: python

    # Insert a custom footer
    (
        "all",
        "footer_slot",
        """
        {
          op: PLUGIN_OPERATIONS.Insert,
          widget: {
            id: 'custom_footer',
            type: DIRECT_PLUGIN,
            RenderWidget: () => (
              <h1>This is the footer.</h1>
            ),
          },
        }"""
    )

That's it!  If you rebuild the ``mfe`` image after enabling the plugin (via ``tutor images build mfe`` or ``tutor local launch``), "This is the footer." should appear at the bottom of every MFE.

It's also possible to target a specific MFE's footer. For instance:

.. code-block:: python

    PLUGIN_SLOTS.add_items([
        # Hide the custom footer
        (
            "profile",
            "footer_slot",
            """
            {
              op: PLUGIN_OPERATIONS.Hide,
              widgetId: 'custom_footer',
            }"""
        ),
        # Insert a footer just for the Profile MFE
        (
            "profile",
            "footer_slot",
            """
            {
              op: PLUGIN_OPERATIONS.Insert,
              widget: {
                id: 'custom_profile_footer',
                type: DIRECT_PLUGIN,
                RenderWidget: () => (
                  <h1>This is the Profile MFE's footer.</h1>
                ),
              },
            }"""
        )
    ])

Note that here we're assuming you didn't remove the global footer configuration defined by the filter items targeting ``"all"``, so you have to hide ``custom_footer`` instead of ``default_contents``.  If you were to rebuild the MFE image now, the Profile MFE's footer would say "This is the Profile MFE's footer", whereas all the others would still contain the global "This is the footer." message.

For more complex frontend plugins, you should make use of ``mfe-env-config-*`` patches to define your JSX components separately. You can create an NPM plugin package, install it via ``mfe-dockerfile-post-npm-install``, import the desired components via ``mfe-env-config-buildtime-imports``, and refer to them with the ``PLUGIN_SLOTS`` filter.

For instance:

.. code-block:: python

    from tutormfe.hooks import PLUGIN_SLOTS
    from tutor import hooks
    
    hooks.Filters.ENV_PATCHES.add_item(
        (
            "mfe-dockerfile-post-npm-install",
            """
    # npm package
    RUN npm install react-loader-spinner
    """,
        )
    )
    
    hooks.Filters.ENV_PATCHES.add_item(
        (
            "mfe-env-config-buildtime-imports",
            """
    import { FidgetSpinner } from 'react-loader-spinner';
    """,
        )
    )
    
    PLUGIN_SLOTS.add_items(
        [
            (
                "learner-dashboard",
                "org.openedx.frontend.learner_dashboard.no_courses_view.v1",
                """
                {
                  op: PLUGIN_OPERATIONS.Hide,
                  widgetId: 'default_contents',
                }"""
            ),
            (
                "learner-dashboard",
                "org.openedx.frontend.learner_dashboard.no_courses_view.v1",
                """
                {
                  op: PLUGIN_OPERATIONS.Insert,
                  widget: {
                    id: 'no_courses_fidget_spinner',
                    type: DIRECT_PLUGIN,
                    RenderWidget: FidgetSpinner,
                  },
                }""",
            ),
        ]
    )


Refer to the `patch catalog <#template-patch-catalog>`_ below for more details.


Hosting extra static files
~~~~~~~~~~~~~~~~~~~~~~~~~~

The MFE plugin allows other plugins to serve extra static files through the MFE service. This enables hosting custom assets (CSS, images, JavaScript, themes, etc.) directly alongside MFE applications, without rebuilding the core MFE image. Assets are exposed via a dedicated volume, so updates can be deployed dynamically via simple pushes to that volume, speeding up tests and updates without full-image builds.

To enable this functionality, set ``MFE_HOST_EXTRA_FILES`` to ``true``:

.. code-block:: bash

    tutor config save --set MFE_HOST_EXTRA_FILES=true

When this setting is enabled, the configured volume patches (explained below) will be applied in all environments so that extra files can be served. In development mode it will additionally expose port ``8002`` on the ``mfe`` service, allowing direct access to those files. In production deployments, port mapping is not required since files are served through Caddy.

Then add your static files using volume patches. For local deployments, use the ``mfe-volumes`` patch:

.. code-block:: python

    from tutor import hooks

    hooks.Filters.ENV_PATCHES.add_item(
        (
            "mfe-volumes",
            """
            - /path/to/static/files:/usr/share/caddy/myfiles:ro
            """
        )
    )

For Kubernetes deployments, use the ``mfe-k8s-volumes`` patch to define the volumes you need, and mount them using the ``mfe-k8s-volume-mounts`` patch:

For example, to mount a ConfigMap at ``/usr/share/caddy/myfiles`` so it’s served at ``/myfiles/*``:

.. code-block:: python

    from tutor import hooks

    hooks.Filters.ENV_PATCHES.add_items(
        [
            (
                "mfe-k8s-volumes",
                """
                - name: myfiles-volume
                  configMap:
                    name: myfiles-configmap
                """
            ),
            (
                "mfe-k8s-volume-mounts",
                """
                - name: myfiles-volume
                  mountPath: /usr/share/caddy/myfiles
                  readOnly: true
                """
            ),
        ]
    )

Your static files will be accessible at ``http(s)://{{ MFE_HOST }}/myfiles/``.

For advanced routing configurations, you can use the ``mfe-caddyfile`` patch to define custom Caddy rules for handling your static files:

.. code-block:: python

    hooks.Filters.ENV_PATCHES.add_item(
        (
            "mfe-caddyfile",
            """
            # Custom routing for static files
            handle_path /myfiles/* {
                root * /usr/share/caddy/myfiles
                file_server
            }
            """
        )
    )


Installing from a private npm registry
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In case you need to install components from a private NPM registry, you can append the ``--registry`` option to your install statement or add a ``npm config set`` command to the plugin.
In some cases, for example when using `GitLab's NPM package registry <https://docs.gitlab.com/ee/user/packages/npm_registry/>`_, you might also need to provide a token for your registry, which can be done with an additional ``npm config set`` command as well:

.. code-block:: python

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

Then, access http://apps.local.openedx.io:1995/profile/u/YOURUSERNAME

You can also bind-mount your own fork of an MFE. For example::

    tutor mounts add /path/to/frontend-app-profile
    tutor dev launch

.. note::

  The name of the bind-mount folder needs to match the name of the repository word-for-word. If you've forked an MFE repository with a custom name, be sure to change the name back to ensure the bind-mount works properly.

With this change, the "profile-dev" image will be automatically re-built during ``launch``. Your host repository will then be bind-mounted at runtime in the "profile" container. This means that changes you make to the host repository will be automatically picked up and hot-reloaded by your development server.

This works for custom MFEs, as well. For example, if you added your own MFE named frontend-app-myapp, then you can bind-mount it like so::

    tutor mounts add /path/to/frontend-app-myapp

.. note::

  Docker tries to run as many build processes in parallel as possible, but this can cause failures in the MFE image build.  If you're running into OOM issues, RAM starvation, or network failures during NPM installs, try the following before restarting::

    cat >buildkitd.toml <<EOF
    [worker.oci]
      max-parallelism = 1
    EOF
    docker buildx create --use --name=singlecpu --config=./buildkitd.toml

Deploying Changes to Production
-------------------------------

You will need to rebuild the mfe Docker image with your changes, and then deploy it to production - exactly how depends on whether you are running ``tutor local`` or ``tutor k8s``.

Provided the modified codebase is mounted in the same machine where production deployment happens, run ``tutor images build mfe`` and restart your local deployment via ``tutor local stop && tutor local start -d``.

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

This is the list of all patches used across tutor-mfe (outside of any plugin). Alternatively, you can search for patches in tutor-mfe templates by grepping the source code:

.. code-block:: python

    git clone https://github.com/overhangio/tutor-mfe
    cd tutor-mfe
    git grep "{{ patch" -- tutormfe/templates

mfe-env-config-buildtime-imports
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use this patch for any static imports you need in ``env.config.jsx``. They will be available here if you used the `mfe-docker-post-npm-install patch <#mfe-docker-post-npm-install>`_ to install an NPM package for all MFEs.

It gets rendered at the very top of the file. You should use normal `ES6 import syntax <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/import>`_.

Note that if you want to only import a module for a particular MFE, doing it here won't work: you'll probably want to use the ``mfe-env-config-runtime-definitions-{}`` patch described below.

File changed: ``tutormfe/templates/mfe/build/mfe/env.config.jsx``

mfe-env-config-buildtime-definitions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use this patch for arbitrary ``env.config.jsx`` javascript code that gets evaluated at build time. It is particularly useful for defining slightly more complex components for use in plugin slots.

There's no version of this patch that runs per MFE.  If you want to define MFE-specific code, you should use the MFE-specific ``mfe-env-config-runtime-definitions-{}`` to achieve the same effect.

File changed: ``tutormfe/templates/mfe/build/mfe/env.config.jsx``

mfe-env-config-runtime-definitions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This patch gets rendered inside an ``async`` function in ``env.config.jsx`` that runs in the browser, allowing you to define conditional imports for external modules that may only be available at runtime. Just make sure to use `import() function <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/import>`_ syntax:

.. code-block:: javascript

    const mymodule1 = await import('mymodule1');
    const { default: myComponent } = await import('mymodule2');

Note the second line in the example above: default module exports work a little differently with ``import()``.  To use the default export you can destructure the imported module, but you have to explicitly rename the ``default`` key, as `documented in MDN <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/import#importing_defaults>`_.

Warning: if the dynamic import of a module fails for whatever reason, ``env.config.jsx`` execution will fail silently.

File changed: ``tutormfe/templates/mfe/build/mfe/env.config.jsx``

mfe-env-config-runtime-definitions-{}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

With this patch you can conditionally import modules or define code for specific MFEs in ``env.config.jsx``. This is a useful place to put an import if you're using the ``mfe-docker-post-npm-install-*`` patch to install a plugin that only works on a particular MFE.

As above, make sure to use the ``import()`` function.

File changed: ``tutormfe/templates/mfe/build/mfe/env.config.jsx``

mfe-env-config-runtime-final
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

At this point, ``env.config.jsx`` is ready to return the ``config`` object to the initialization code at runtime. You can use this patch to do anything to the object, including using modules that were imported dynamically earlier.

File changed: ``tutormfe/templates/mfe/build/mfe/env.config.jsx``

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

mfe-dockerfile-base
~~~~~~~~~~~~~~~~~~~

Add Dockerfile instructions that will be applied to the base layer of the "mfe" image. This base layer is used both in production and development, for all applications.

File changed: ``tutormfe/templates/mfe/build/mfe/Dockerfile``

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

Add custom configurations to the internal MFE Caddyfile.  
Patches defined here are rendered **inside** the ``:8002 { ... }`` server block of the MFE container, before the default reverse proxies and route handlers are applied.

Note: This patch modifies the **internal MFE application server** (running in the ``mfe`` container). It is distinct from the ``caddyfile-mfe-proxy`` patch, which updates the **public-facing proxy** Caddyfile under ``apps.LMS_HOST``.

For a complete list of supported directives, consult the Caddy `Directives <https://caddyserver.com/docs/caddyfile/directives>`_ documentation. 

File changed: ``tutormfe/templates/mfe/apps/mfe/Caddyfile``

mfe-volumes
~~~~~~~~~~~

Add volumes to the mfe service in local Docker Compose deployment.

File changed: ``local/docker-compose.yml``

mfe-k8s-volumes
~~~~~~~~~~~~~~~

Add volumes to the mfe deployment in Kubernetes.

File changed: ``k8s/deployments.yml``


mfe-k8s-volume-mounts
~~~~~~~~~~~~~~~~~~~~~

Add volume mounts to the ``mfe`` container in the Kubernetes deployment. Use this together with ``mfe-k8s-volumes`` to attach and mount custom volumes (e.g., ConfigMaps, PVCs) inside the container.

File changed: ``k8s/deployments.yml``


caddyfile-mfe-proxy
~~~~~~~~~~~~~~~~~~~

Add any custom configurations for the ``caddyfile-mfe-proxy``.  
Patches defined here are added to ``/.local/share/tutor/env/apps/caddy/Caddyfile`` under the public-facing MFE apps server block (e.g., ``apps.LMS_HOST``).

Note: This patch applies to the proxy handler for all MFEs and does not target any specific MFE. It is functionally distinct from the ``mfe-caddyfile`` patch.

Its usage is functionally equivalent to that of the `caddyfile-lms <https://github.com/overhangio/tutor/blob/release/docs/reference/patches.rst#caddyfile-lms>`_ and `caddyfile-cms <https://github.com/overhangio/tutor/blob/release/docs/reference/patches.rst#caddyfile-cms>`_ patches.

For a complete list of supported directives, consult the Caddy `Directives <https://caddyserver.com/docs/caddyfile/directives>`_ documentation.

Example: The following patch adds a ``respond`` directive so that visitors requesting ``apps.LMS_HOST/robots.txt`` receive a disallow response:

.. code-block:: python

    from tutor import hooks

    hooks.Filters.ENV_PATCHES.add_item(
        (
            "caddyfile-mfe-proxy",
            """
    # Serve robots.txt
    respond /robots.txt 200 {
        body "User-agent: *
    Disallow: /"
        close
    }
            """
        )
    )

File changed: ``tutormfe/patches/caddyfile``



Troubleshooting
---------------

NPM Dependency Conflict When overriding ``@edx/frontend-component-header`` or ``@edx/frontend-component-footer``
----------------------------------------------------------------------------------------------------------------

When there is a need to customize the ``@edx/frontend-component-header`` or ``@edx/frontend-component-footer`` component, there is a chance that npm dependency conflicts can occur. In the case of such a conflict, perform the following to resolve the conflicts while keeping the customizations in place:

1. Identify your openedx version, for example, ``quince``.
2. Navigate to `Learning <https://github.com/openedx/frontend-app-learning>`_ and `Learner Dashboard <https://github.com/openedx/frontend-app-learner-dashboard>`_ MFEs repositories and checkout to branch ``open-release/quince.master``. Inspect which header and footer versions are installed from ``package.json``. Learning and Learner Dashboard MFEs are mentioned only as an example. Hence, This step can be applied to all MFEs.
3. Determine the versions of ``@edx/frontend-platform`` used in MFEs. Also, check that the header/footer you plan to customize is compatible with the same version of ``@edx/frontend-platform`` specified in their ``package.json`` file (peer-dependencies).
4. Ensure consistency between the versions. For example, If MFE has ``@edx/frontend-platform: 7.0.1``, then customize the header/footer component which has ``@edx/frontend-platform: ^7.0.0`` in ``package.json`` under peer-dependencies
5. Checkout to that specific tag (e.g: ``v7.0.0``) of header component and customize it
6. Install the customized header/footer components into your MFEs. This will resolve any npm dependency conflict issues.
7. All the steps outlined above need to be followed for the footer as well, if you have followed them for the header or vice versa.

.. image:: https://raw.githubusercontent.com/overhangio/tutor-mfe/release/media/npm-conflict-deps.png
    :alt: Observation of MFE header and footer versions

From the above image, it can be observed that ``master`` branch of Learning MFE uses ``@edx/platform@5.6.1`` and Discussions MFE uses ``@edx/platform@7.1.0``. If customized header is created from ``master`` branch, it ensures compatibility with the Discussions MFE as header module supports ``@edx/platform@^7.0.0``. However, the customized header triggers npm dependencies conflit error for learning MFE.
In this case, checkout custom branch from ``v4.11.1`` of header for Learning MFE and ``v5.0.0`` for Discussions MFE. You can install your customized header versions in their respective MFEs as shown below::

    hooks.Filters.ENV_PATCHES.add_items(
        [
            (
                "mfe-dockerfile-post-npm-install-learning",
                """
        RUN npm install '@edx/frontend-component-header@npm:@custom/frontend-component-header@^4.11.1'
        """
            ),
            (
                "mfe-dockerfile-post-npm-install-discussions",
                """
        RUN npm install '@edx/frontend-component-header@npm:@custom/frontend-component-header@^5.0.0'
        """
            ),
        ]
    )


This Tutor plugin is maintained by Adolfo Brandes from `Axim <https://openedx.atlassian.net/wiki/spaces/COMM/pages/3554082883/Axim+Collaborative>`__. Community support is available from the official `Open edX forum <https://discuss.openedx.org>`__. Do you need help with this plugin? See the `troubleshooting <https://docs.tutor.edly.io/troubleshooting.html>`__ section from the Tutor documentation.

License
-------

This software is licensed under the terms of the `GNU Affero General Public License (AGPL) <https://github.com/overhangio/tutor-mfe/blob/release/LICENSE.txt>`_.
