Micro Frontend base plugin for `Tutor <https://docs.tutor.edly.io>`__
=========================================================================

This plugin makes it possible to easily add micro frontend (MFE) applications on top of an Open edX platform that runs with Tutor. To learn more about MFEs, please check the `official Open edX documentation <https://openedx.github.io/frontend-platform/>`__.

In addition, this plugin comes with a few MFEs which are enabled by default:

- `Admnistrator Console <https://github.com/openedx/frontend-app-admin-console/>`__
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
- `Catalog <https://github.com/openedx/frontend-app-catalog/>`__
- `Instructor Dashboard <https://github.com/openedx/frontend-app-instructor-dashboard/>`__

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

Administrator Console
~~~~~~~~~~~~~~~~~~~~~

.. image:: https://raw.githubusercontent.com/overhangio/tutor-mfe/release/media/admin-console.png
    :alt: Account MFE screenshot

An MFE to manage platform-level settings and administrative tasks. To manage library teams, go to ``http(s)://{{ MFE_HOST }}/admin-console/authz/libraries/{{ LIBRARY_ID }}``. 

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

Catalog
~~~~~~~~

.. image:: https://raw.githubusercontent.com/overhangio/tutor-mfe/release/media/catalog.png
    :alt: Catalog MFE screenshot

The Catalog MFE replaces the former Home, Course About and Course catalog pages, which is the main part of the LMS where students start interacting with courses.

Instructor Dashboard
~~~~~~~~~~~~~~~~~~~~

.. image:: https://raw.githubusercontent.com/overhangio/tutor-mfe/release/media/instructor-dashboard.png
    :alt: Instructor Dashboard screenshot

The Instructor Dashboard app provides course staff with a unified interface for managing a course, including enrollments, cohorts, grading, bulk email, and other administrative tasks.

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

.. note::

   If you're using frontend-base apps, see `Using Frontend Slots`_ or `Using App Packages for Slot Operations`_ below for the newer mechanisms.

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


Configuring External Scripts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

External scripts are a feature of both frontend-platform (for legacy MFEs, via ``env.config.jsx``) and frontend-base (for the site, via ``customApp``) that allows script loaders to run when an app boots. A loader is a JavaScript class with a ``constructor({ config })`` and a ``loadScript()`` method. This plugin provides the ``EXTERNAL_SCRIPTS`` hook so that Tutor plugins can register loaders for either target without resorting to patches.

The hook works similarly to ``PLUGIN_SLOTS``. Each item is a tuple of ``(target, loader_class)``, where ``target`` is one of:

- the name of a specific MFE (applies to that MFE only),
- ``"site"`` (applies only to the frontend-base site),
- ``"all"`` (applies to every legacy MFE and the site).

``loader_class`` is the name of a loader class. The framework instantiates it at runtime and passes the app's runtime config to its constructor.

For instance, to inject a third-party ``<script>`` tag across all MFEs, define a loader directly in ``env.config.jsx``:

.. code-block:: python

    from tutormfe.hooks import EXTERNAL_SCRIPTS
    from tutor import hooks

    hooks.Filters.ENV_PATCHES.add_item(
        (
            "mfe-env-config-buildtime-definitions",
            """
    class CustomScriptLoader {
      constructor({ config }) {
        this.config = config;
      }

      loadScript() {
        if (!this.config.CUSTOM_SCRIPT_URL) {
          return;
        }
        const script = document.createElement('script');
        script.id = 'custom-script';
        script.src = this.config.CUSTOM_SCRIPT_URL;
        document.head.appendChild(script);
      }
    }
    """,
        )
    )

    EXTERNAL_SCRIPTS.add_items([
        (
            "all",
            "CustomScriptLoader",
        ),
    ])

The ``CustomScriptLoader`` class is defined via the ``mfe-env-config-buildtime-definitions`` patch, and the ``EXTERNAL_SCRIPTS`` hook wires it into the configuration. Frontend-platform instantiates the class at runtime and passes the MFE's runtime config to the constructor, so the loader can read any key from ``MFE_CONFIG`` (here, ``CUSTOM_SCRIPT_URL``, which you would set via the ``mfe-lms-common-settings`` patch or equivalent). The built-in ``GoogleAnalyticsLoader`` in ``@openedx/frontend-platform/scripts`` follows the same pattern with ``config.GOOGLE_ANALYTICS_4_ID`` - you can import it with the ``mfe-env-config-buildtime-imports`` patch and use it with ``EXTERNAL_SCRIPTS`` in the same way.

You can also target a specific MFE. For example, to load a custom script only on the learning MFE:

.. code-block:: python

    from tutormfe.hooks import EXTERNAL_SCRIPTS
    from tutor import hooks

    hooks.Filters.ENV_PATCHES.add_item(
        (
            "mfe-dockerfile-post-npm-install",
            """
    RUN npm install @myorg/custom-script-loader
    """,
        )
    )

    hooks.Filters.ENV_PATCHES.add_item(
        (
            "mfe-env-config-buildtime-imports",
            """
    import { CustomScriptLoader } from '@myorg/custom-script-loader';
    """,
        )
    )

    EXTERNAL_SCRIPTS.add_items([
        (
            "learning",
            "CustomScriptLoader",
        ),
    ])

Note that if no external scripts are configured, the ``externalScripts`` key is not set in the MFE config at all, so any MFE-level defaults are preserved.

To register a loader on the frontend-base site, use the ``mfe-site-custom-app-definitions`` and ``mfe-site-custom-app-imports`` patches in place of their ``mfe-env-config-buildtime-*`` equivalents, and target ``"site"`` (or ``"all"``) in ``EXTERNAL_SCRIPTS``. The loader's ``constructor({ config })`` receives the ``customApp`` runtime configuration, which you can populate via the site config (for example, through ``commonAppConfig``) or the ``runtimeConfigJsonUrl`` endpoint.


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

Frontend-base site
------------------

In addition to hosting individual MFEs, this plugin supports `frontend-base <https://github.com/openedx/frontend-base>`__, a unified framework for Open edX frontend apps. In practice, frontend-base is a replacement for ``frontend-build``, ``frontend-platform``, ``frontend-plugin-framework``, ``frontend-component-header``, and ``frontend-component-footer``. It enables apps to be loaded as direct plugins within a single, unified application (the "shell"), rather than as separate, independently deployed micro frontends. Some key advantages:

- For all Tutor users: shared dependencies (React, Paragon, etc.) are installed and built only once, speeding up builds and reducing page load times.
- For learners: deduped dependencies prevent UX inconsistencies, and navigation between apps no longer triggers full page refreshes.
- For plugin authors: frontend apps are plugins themselves; the same API can be used to create Tutor plugins, including ones that add entire new routes.
- For frontend developers: there's a single `mfe-dev` Docker service for all apps, but individual ones (as well as the site itself) can still be mounted and developed independently.
- For tutor-mfe developers: everything about the frontend-base site is considered user configuration, from package.json to index.html; no monkey-patching required.

When frontend apps are enabled, the plugin builds a frontend-base site that bundles them together into a shell application. The site is served by the same ``mfe`` container alongside legacy MFEs, with Caddy routing requests appropriately.

Frontend apps
~~~~~~~~~~~~~

Frontend apps are npm packages that plug into the frontend-base site. This plugin ships with four core frontend apps:

- ``authn`` (``@openedx/frontend-app-authn``): disabled by default
- ``learner-dashboard`` (``@openedx/frontend-app-learner-dashboard``): disabled by default
- ``instructor-dashboard`` (``@openedx/frontend-app-instructor-dashboard``): enabled by default
- ``notifications`` (``@openedx/frontend-app-notifications``): enabled by default

To enable apps, use the ``tutormfe.hooks.FRONTEND_APPS`` filter:

.. code-block:: python

    from tutormfe.hooks import FRONTEND_APPS

    @FRONTEND_APPS.add()
    def _enable_core_apps(apps):
        apps["authn"]["enabled"] = True
        apps["learner-dashboard"]["enabled"] = True
        return apps

Note that if an enabled frontend app matches a legacy MFE, the legacy MFE will be effectively disabled.  This is the case with both Authn and Learner Dashboard if the example above is followed.

Enabling or disabling existing apps does not require rebuilding tutor-mfe images: after a `tutor config save`, only a Tutor restart is required.

To add a custom frontend app (which does require rebuilding), the Tutor plugin would be:

.. code-block:: python

    from tutormfe.hooks import FRONTEND_APPS

    from tutor import hooks

    @FRONTEND_APPS.add()
    def _add_my_app(apps):
        apps["my-app"] = {
            "npm_package": "@myorg/frontend-app-my-app",
            "npm_version": "^1.0.0",
            "enabled": True,
        }
        return apps

    hooks.Filters.ENV_PATCHES.add_items(
        [
            (
                "mfe-site-config-imports",
                """
    import { myApp } from '@myorg/frontend-app-my-app';
    """
            ),
            (
                "mfe-site-config",
                """
    addApp(siteConfig, myApp);
    """
            ),
        ]
    )

Optionally, a ``source`` key can be added to the app dictionary. If ``source`` is present, it will be used at build time instead of installing from NPM.

``source`` accepts two shapes:

- A git URL (``https://...``, ``git@...``) - cloned at build time. An optional git ref can be pinned with the standard ``#<ref>`` suffix (e.g. ``https://github.com/myorg/frontend-app-my-app.git#my-branch``). Without the suffix, the repository's default branch is used.
- A ``file://`` URL (e.g. ``file://site/packages/frontend-app-my-app``) - the path, relative to the tutor-mfe build context, is copied at build time. Tutor plugins can render templates into this path to ship an app's source alongside the plugin itself.

Runtime configuration
~~~~~~~~~~~~~~~~~~~~~

By default, the frontend-base site fetches its runtime configuration from the LMS at ``/api/frontend_site_config/v1/``. This configuration is populated from the ``FRONTEND_SITE_CONFIG`` dictionary in the LMS settings.

Tutor-mfe automatically populates ``FRONTEND_SITE_CONFIG`` with base URLs, login/logout URLs, external routes, and per-app configuration. To add custom values or override existing ones, use the ``mfe-lms-common-settings``, ``mfe-lms-production-settings``, or ``mfe-lms-development-settings`` patches:

.. code-block:: python

    from tutor import hooks

    hooks.Filters.ENV_PATCHES.add_item(
        (
            "mfe-lms-common-settings",
            """
    FRONTEND_SITE_CONFIG["supportUrl"] = "https://support.example.com"
    FRONTEND_SITE_CONFIG["commonAppConfig"]["MY_CUSTOM_SETTING"] = "my-value"
    """
        )
    )

Backward compatibility with MFE_CONFIG
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Note that for maximum backward compatibility, the ``/api/frontend_site_config/v1/`` endpoint automatically converts existing ``MFE_CONFIG`` and ``MFE_CONFIG_OVERRIDES`` configuration (including that pulled from Django's ``site_configuration`` model) to frontend-base's SiteConfig structure, where applicable. However, it does so with a lower precedence than ``FRONTEND_SITE_CONFIG``. This means explicit FRONTEND_SITE_CONFIG entries will always override ``MFE_CONFIG`` ones, including those coming from the database.  If database configuration or backward compatibility are priorities, empty the ``FRONTEND_SITE_CONFIG`` dictionary using the ``mfe-lms-common-settings`` patch:

.. code-block:: python

    from tutor import hooks

    hooks.Filters.ENV_PATCHES.add_item(
        (
            "mfe-lms-common-settings",
            """
    FRONTEND_SITE_CONFIG = {}
    """
        )
    )

Domain-dependent runtime configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For domain-dependent runtime configuration without rebuilding the tutor-mfe images, you can use the `extra static files <#hosting-extra-static-files>`_ feature together with a ``mfe-caddyfile`` patch to serve JSON files instead of proxying to the LMS. For example, to serve per-domain config from ``/usr/share/caddy/site-config/``:

.. code-block:: python

    from tutor import hooks

    hooks.Filters.ENV_PATCHES.add_items(
        [
            (
                "mfe-volumes",
                """
            - /path/to/site-config:/usr/share/caddy/site-config:ro
            """
            ),
            (
                "mfe-caddyfile",
                """
    handle /api/frontend_site_config/v1/ {
        root * /usr/share/caddy/site-config
        rewrite * /{host}.json
        file_server
    }
    """
            ),
        ]
    )

With ``MFE_HOST_EXTRA_FILES`` set to ``true``, this intercepts the runtime config request before it reaches the LMS, and serves a host-specific JSON file (e.g., ``apps.mysite.com.json``) from the mounted volume instead.

Custom runtime configuration URL
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can also point ``runtimeConfigJsonUrl`` to a URI of your choosing via the ``mfe-site-config`` patch:

.. code-block:: python

    from tutor import hooks

    hooks.Filters.ENV_PATCHES.add_item(
        (
            "mfe-site-config",
            """
    siteConfig.runtimeConfigJsonUrl = 'https://cdn.example.com/site-config.json';
    """
        )
    )

Configuration variables
~~~~~~~~~~~~~~~~~~~~~~~

The following Tutor configuration variables control the frontend-base site:

- ``MFE_SITE_PORT`` (default: ``8080``): the port on which the site is served.
- ``MFE_SITE_REPOSITORY`` (default: ``""``): an optional git URL for a custom site repository, to be used instead of the default template.
- ``MFE_SITE_VERSION`` (default: ``""``): the branch or tag to clone from ``MFE_SITE_REPOSITORY``.

Using Frontend Slots
~~~~~~~~~~~~~~~~~~~~

The ``FRONTEND_SLOTS`` filter is the frontend-base equivalent of ``PLUGIN_SLOTS``. Instead of targeting individual MFEs by name, it registers slot operations globally in the site's ``customApp``, where they apply to all frontend apps served by the site.

Each item added to the filter is a string containing a TypeScript ``SlotOperation`` object literal. For example, to replace the default footer with a custom one:

.. code-block:: python

    from tutormfe.hooks import FRONTEND_SLOTS

    FRONTEND_SLOTS.add_items([
        """
        {
          slotId: 'org.openedx.frontend.slot.footer.main.v1',
          op: 'widgetReplace',
          id: 'customFooter',
          relatedId: 'defaultContent',
          element: (
            <h1>This is the footer.</h1>
          ),
        }""",
    ])

Unlike ``PLUGIN_SLOTS``, there's no MFE name parameter - slot operations are applied site-wide. The ``slotId`` field identifies which slot to target, and each operation uses the ``SlotOperation`` format defined by `@openedx/frontend-base <https://github.com/openedx/frontend-base/>`_. Widget operations include ``widgetAppend``, ``widgetPrepend``, ``widgetInsertBefore``, ``widgetInsertAfter``, ``widgetReplace``, ``widgetRemove``, and ``widgetOptions``. Layout operations include ``layoutReplace`` and ``layoutOptions``.

You can also use the ``mfe-site-custom-app-final`` and ``mfe-site-custom-app-imports`` patches to add arbitrary code directly to ``customApp.tsx``, bypassing the filter entirely.

Note that the examples above use string literals like ``'widgetRemove'`` rather than the ``WidgetOperationTypes`` constants shown in the app package section below. Using the constants would require adding an import via ``mfe-site-custom-app-imports``, which isn't worth the trouble here - the string values are equivalent.

``FRONTEND_SLOTS`` is best suited for simple slot operations or as an easier migration path from ``PLUGIN_SLOTS``. For more complex frontend plugins, you should create an npm app package instead (see below).

Using App Packages for Slot Operations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For anything beyond simple slot manipulations, the recommended approach is to create an npm app package that exports an ``App`` object with its own ``slots`` array. This is the same pattern used by frontend-base's built-in apps (like the shell, header, and footer), and it keeps your slot logic, components, and styles together in a self-contained package.

An app package is a regular npm package that exports an ``App`` object. For example, a package called ``@myorg/my-frontend-plugin`` might contain:

.. code-block:: typescript

    // src/app.tsx
    import { App, WidgetOperationTypes } from '@openedx/frontend-base';
    import { FidgetSpinner } from 'react-loader-spinner';

    const app: App = {
      appId: 'myFrontendPlugin',
      slots: [
        {
          slotId: 'org.openedx.frontend.slot.learnerDashboard.noCoursesView.v1',
          op: WidgetOperationTypes.REPLACE,
          id: 'noCoursesFidgetSpinner',
          relatedId: 'defaultContent',
          component: FidgetSpinner,
        },
      ],
    };

    export default app;

Then, in your Tutor plugin, install the package and register it via the site config:

.. code-block:: python

    from tutor import hooks

    hooks.Filters.ENV_PATCHES.add_item(
        (
            "mfe-dockerfile-post-npm-install-site",
            """
    RUN npm install @myorg/my-frontend-plugin
    """,
        )
    )

    hooks.Filters.ENV_PATCHES.add_item(
        (
            "mfe-site-config-imports",
            """
    import myFrontendPlugin from '@myorg/my-frontend-plugin';
    """,
        )
    )

    hooks.Filters.ENV_PATCHES.add_item(
        (
            "mfe-site-config",
            """
    addApp(siteConfig, myFrontendPlugin);
    """,
        )
    )

This approach keeps your components, styles, and slot operations in a proper package with its own dependencies, tests, and build pipeline, rather than inlining everything through template patches.

Compat shim for FPF-built plugins
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some Tutor plugins ship slot contributions written against the legacy ``frontend-plugin-framework`` API, and many plugin packages still import from ``@edx/frontend-platform``. To make those work on a frontend-base site without requiring each plugin to be ported first, tutor-mfe renders one compatibility module per MFE (``env.config.<mfe_name>.jsx``) and wires each one into the site as its own shim App via `@openedx/frontend-base-compat <https://github.com/openedx/frontend-base-compat>`__. The shim translates legacy slot contributions into frontend-base slot operations, and ``site/package.json`` aliases both ``@openedx/frontend-plugin-framework`` and ``@edx/frontend-platform`` as direct dependencies pointing at the shim package, so any FPF- or frontend-platform-built dependency installed transitively also resolves to the shim's drop-in stubs and neither real package is installed.

The shim does not translate ``PLUGIN_SLOTS`` contributions automatically: site operators or plugin authors choose which contributions to route through it, since not every legacy contribution survives the translation cleanly. The legacy per-MFE ``env.config.jsx`` continues to consume ``PLUGIN_SLOTS`` unchanged, so standalone legacy MFEs render the contribution exactly as before whether or not it is opted in to the shim.

The coarsest opt-in is by plugin name: ``FRONTEND_COMPAT_PLUGINS`` takes a Tutor plugin name and folds every ``PLUGIN_SLOTS`` contribution registered in that plugin's hook context into the compat shim, regardless of which legacy MFE each contribution targeted. This is useful when wrapping a third-party plugin you don't control (a meta-plugin can opt the whole thing in without touching the upstream code), or when you'd rather not enumerate every slot in your own plugin:

.. code-block:: python

    from tutormfe.hooks import FRONTEND_COMPAT_PLUGINS

    FRONTEND_COMPAT_PLUGINS.add_item("some-legacy-plugin")

The tradeoff is bluntness: every slot that plugin contributes goes through the shim, including any whose translation isn't covered by the default maps, so failures surface at bundle time rather than as a clear "this slot isn't supported yet" signal.

For finer control, ``FRONTEND_COMPAT_SLOTS`` opts in one ``(mfe_name, slot_name, plugin_config)`` triple at a time. Use this when you want explicit per-slot acknowledgement, when only some of a plugin's contributions translate cleanly, or when you want to ship the same contribution to legacy MFEs and the compat shim from a single source:

.. code-block:: python

    from tutormfe.hooks import PLUGIN_SLOTS, FRONTEND_COMPAT_SLOTS

    MY_SLOT = (
        "course_outline_sidebar.v1",
        """
        {
          op: PLUGIN_OPERATIONS.Insert,
          widget: {
            id: 'my-widget',
            type: DIRECT_PLUGIN,
            RenderWidget: MyComponent,
          }
        }
        """,
    )

    PLUGIN_SLOTS.add_item(("learning", *MY_SLOT))
    FRONTEND_COMPAT_SLOTS.add_item(("learning", *MY_SLOT))

``FRONTEND_COMPAT_SLOTS`` carries the same ``mfe_name`` field as ``PLUGIN_SLOTS``, so each contribution is routed to the per-MFE compat module rendered for that MFE and ends up in the legacy app the shim mounts for it. To target multiple MFEs from one source, register one triple per MFE. Once a plugin ships a native ``FRONTEND_SLOTS`` (or app-package) contribution for the same slot, drop the ``FRONTEND_COMPAT_SLOTS`` entry to avoid rendering the widget twice.

All compat wiring is gated on at least one ``(mfe_name, slot_name, plugin_config)`` triple actually resolving through these filters: vanilla sites, and sites whose opt-ins resolve to no contributions (e.g., a named plugin that ships no ``PLUGIN_SLOTS``), skip the shim wiring entirely and pay no overhead. MFEs with no opted-in contributions get no compat module and no legacy app on the site.

``FRONTEND_ROUTE_COMPAT_MAPS`` layers ``(mfe_id, route_roles)`` deltas on top of the shim's ``defaultRouteMap``. Use it to declare which frontend-base route roles a legacy MFE renders for, so the shim can scope a legacy app's contributions to the right routes. ``route_roles`` is a JSON-serializable list of role-id strings:

.. code-block:: python

    from tutormfe.hooks import FRONTEND_ROUTE_COMPAT_MAPS

    FRONTEND_ROUTE_COMPAT_MAPS.add_items([
        ("my-legacy-mfe", ["org.openedx.frontend.role.myCustomRole"]),
    ])

``FRONTEND_SLOT_COMPAT_MAPS`` and ``FRONTEND_WIDGET_COMPAT_MAPS`` follow the same shape but layer ``(legacy_id, mapping)`` deltas on top of the shim's built-in ``defaultSlotMap`` / ``defaultWidgetMap``. Use them when a plugin's ``PLUGIN_SLOTS`` contribution targets a legacy slot id that the shim doesn't yet cover, or to override a curated mapping site-locally. ``mapping`` is a JSON-serializable dict matching the shim's ``SlotMappingEntry`` / ``WidgetMappingEntry`` shape (see the shim's ADR for the full schema):

.. code-block:: python

    from tutormfe.hooks import FRONTEND_SLOT_COMPAT_MAPS

    FRONTEND_SLOT_COMPAT_MAPS.add_items([
        ("org.openedx.frontend.aspects.course_outline_sidebar.v1", {
            "targetSlotId": "org.openedx.frontend.slot.aspects.outlineSidebar.v1",
        }),
    ])

Identical contributions for the same legacy id are deduplicated silently. Divergent contributions emit a ``tutor config save`` warning and last-wins, so a transient conflict during a plugin upgrade still produces a working bundle.

Frontend-base site development
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can bind-mount individual frontend app repositories for concurrent development. For example, if you have a local checkout of a frontend-base-compatible ``frontend-app-learner-dashboard``::

    tutor mounts add /path/to/frontend-app-learner-dashboard
    tutor dev launch

An ``mfe-dev`` hot-loading service will be started with the app's source bind-mounted as an npm workspace package, so changes to it are picked up automatically. The site will be available at ``http://apps.local.openedx.io:8080``.

You can also develop the frontend-base site locally by bind-mounting a ``frontend-site`` directory.  However, contrary to the ``frontend-app-*`` repositories, there is no upstream ``frontend-site`` equivalent. (The Open edX project considers it to be a downstream configuration concern, which is why tutor-mfe implements it internally.) There is, however, a template repository, `frontend-template-site <https://github.com/openedx/frontend-template-site>`__, you can clone locally for this purpose::

    git clone https://github.com/openedx/frontend-template-site.git frontend-site

Then::

    tutor mounts add /path/to/frontend-site
    tutor dev launch

If you want to develop a core frontend-base app as an independent SPA, it's still possible to do so.  You just have to make sure the app is not enabled, which will cause Tutor to treat it as a standalone MFE.  Since core frontend apps are disabled by default, this is the default behavior.  If you've previously enabled an app and want to revert it, set ``enabled`` to ``False``.  Image rebuilding is not necessary.

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

mfe-site-config-imports
~~~~~~~~~~~~~~~~~~~~~~~

Add static TypeScript/ES6 imports to both the production and development site config files. Use this to import frontend app modules that will be added to the site via the ``mfe-site-config`` patch.

File changed: ``tutormfe/templates/mfe/build/mfe/site/site.config.build.tsx``, ``tutormfe/templates/mfe/build/mfe/site/site.config.dev.tsx``

mfe-site-config-imports-production
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add static imports only to the production site config file.

File changed: ``tutormfe/templates/mfe/build/mfe/site/site.config.build.tsx``

mfe-site-config-imports-development
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add static imports only to the development site config file.

File changed: ``tutormfe/templates/mfe/build/mfe/site/site.config.dev.tsx``

mfe-site-config
~~~~~~~~~~~~~~~

Add arbitrary TypeScript code to both the production and development site config files. Runs after the ``siteConfig`` object is defined, so you can modify it directly (e.g., ``addApp(siteConfig, myApp)``).

File changed: ``tutormfe/templates/mfe/build/mfe/site/site.config.build.tsx``, ``tutormfe/templates/mfe/build/mfe/site/site.config.dev.tsx``

mfe-site-config-production
~~~~~~~~~~~~~~~~~~~~~~~~~~

Add arbitrary TypeScript code only to the production site config file.

File changed: ``tutormfe/templates/mfe/build/mfe/site/site.config.build.tsx``

mfe-site-config-development
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add arbitrary TypeScript code only to the development site config file.

File changed: ``tutormfe/templates/mfe/build/mfe/site/site.config.dev.tsx``

mfe-site-custom-app-imports
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add static ES6 imports for use in the site's ``customApp``.

File changed: ``tutormfe/templates/mfe/build/mfe/site/src/customApp.tsx``

mfe-site-custom-app-definitions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add inline TypeScript/JavaScript declarations (classes, functions, constants) for use in the site's ``customApp``.

File changed: ``tutormfe/templates/mfe/build/mfe/site/src/customApp.tsx``

mfe-site-custom-app-final
~~~~~~~~~~~~~~~~~~~~~~~~~

Add arbitrary code to the site's ``customApp``, such as slot plugin or external script registrations. Components and loader classes imported or defined via ``mfe-site-custom-app-imports`` or ``mfe-site-custom-app-definitions`` can be referenced here.

File changed: ``tutormfe/templates/mfe/build/mfe/site/src/customApp.tsx``

mfe-dockerfile-pre-npm-install-site
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add Dockerfile instructions before the site's ``npm install`` step.

File changed: ``tutormfe/templates/mfe/build/mfe/Dockerfile``

mfe-dockerfile-post-npm-install-site
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add Dockerfile instructions after the site's ``npm install`` step. Use this to install additional npm packages into the site workspace.

File changed: ``tutormfe/templates/mfe/build/mfe/Dockerfile``

mfe-dockerfile-pre-npm-build-site
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add Dockerfile instructions before the site's production build step. Use this to set environment variables or run pre-build scripts.

File changed: ``tutormfe/templates/mfe/build/mfe/Dockerfile``

mfe-dockerfile-post-npm-build-site
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add Dockerfile instructions after the site's production build step.

File changed: ``tutormfe/templates/mfe/build/mfe/Dockerfile``

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

Maintenance
-----------

This Tutor plugin is maintained by Adolfo Brandes from `Axim <https://openedx.atlassian.net/wiki/spaces/COMM/pages/3554082883/Axim+Collaborative>`__. Community support is available from the official `Open edX forum <https://discuss.openedx.org>`__. Do you need help with this plugin? See the `troubleshooting <https://docs.tutor.edly.io/troubleshooting.html>`__ section from the Tutor documentation.

Updating the site lockfile
~~~~~~~~~~~~~~~~~~~~~~~~~~

The site ships with a ``package-lock.json`` that is used at build time to ensure the site's npm install layer is properly cached: when the lockfile changes, the ``npm install`` layer is invalidated and rebuilt. It must be regenerated manually when dependencies change.

Tutor-mfe provides a dedicated command that regenerates it inside a Docker build, so node and npm don't need to be installed on the host:

1. Make sure the plugin is enabled and any ``FRONTEND_APPS`` customizations you want reflected in the lockfile are configured. Then render the templates::

       tutor config save

2. Run the refresh command, pointing ``--output`` at the lockfile inside your tutor-mfe source checkout::

       tutor mfe update-site-lockfile \
           --output /path/to/tutor-mfe/tutormfe/templates/mfe/build/mfe/site/package-lock.json

   If ``--output`` is omitted, the refreshed lockfile is written to ``./package-lock.json`` in the current directory, and you can copy it into the tutor-mfe source tree yourself.

3. Commit the updated ``package-lock.json``.

Under the hood, this command runs ``npm update`` inside the ``site-lockfile-refresh`` Docker build stage, which picks up the latest versions allowed by the existing semver ranges in ``package.json``.

License
-------

This software is licensed under the terms of the `GNU Affero General Public License (AGPL) <https://github.com/overhangio/tutor-mfe/blob/release/LICENSE.txt>`_.
