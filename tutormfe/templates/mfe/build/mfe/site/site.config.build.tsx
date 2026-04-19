import { EnvironmentTypes, SiteConfig, footerApp, headerApp, shellApp } from '@openedx/frontend-base';
import customApp from './src/customApp';
import { addApp, addExternalRoute } from './src/utils';

{% if get_frontend_app("authn") %}
import { authnApp } from '@openedx/frontend-app-authn';
{% endif %}

{% if get_frontend_app("learner-dashboard") %}
import { learnerDashboardApp } from '@openedx/frontend-app-learner-dashboard';
{% endif %}

{% if get_frontend_app("instructor-dashboard") %}
import { instructorDashboardApp } from '@openedx/frontend-app-instructor-dashboard';
{% endif %}

{% if get_frontend_app("notifications") %}
import { notificationsApp } from '@openedx/frontend-app-notifications';
{% endif %}

{{ patch("mfe-site-config-imports") }}
{{ patch("mfe-site-config-imports-production") }}

import '@openedx/frontend-base/shell/style';
import '@edx/brand/core.min.css';
import '@edx/brand/light.min.css';

const siteConfig: SiteConfig = {
  siteId: 'tutor-site',
  siteName: {{ PLATFORM_NAME | tojson }},
  baseUrl: '{{ "https" if ENABLE_HTTPS else "http" }}://{{ MFE_HOST }}',
  lmsBaseUrl: '{{ "https" if ENABLE_HTTPS else "http" }}://{{ LMS_HOST }}',
  loginUrl: '{{ "https" if ENABLE_HTTPS else "http" }}://{{ LMS_HOST }}/login',
  logoutUrl: '{{ "https" if ENABLE_HTTPS else "http" }}://{{ LMS_HOST }}/logout',

  environment: EnvironmentTypes.PRODUCTION,
  apps: [
    shellApp,
    headerApp,
    footerApp,
    customApp,
  ],
  externalRoutes: [],

  runtimeConfigJsonUrl: '/api/frontend_site_config/v1/',
  accessTokenCookieName: 'edx-jwt-cookie-header-payload',
};

{% if get_frontend_app("authn") %}
addApp(siteConfig, authnApp);
{% endif %}

{% if get_frontend_app("learner-dashboard") %}
addApp(siteConfig, learnerDashboardApp);
{% endif %}

{% if get_frontend_app("instructor-dashboard") %}
addApp(siteConfig, instructorDashboardApp);
{% endif %}

{% if get_frontend_app("notifications") %}
addApp(siteConfig, notificationsApp);
{% endif %}

{{ patch("mfe-site-config") }}
{{ patch("mfe-site-config-production") }}

export default siteConfig;
