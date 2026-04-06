import { EnvironmentTypes, SiteConfig, footerApp, headerApp, shellApp } from '@openedx/frontend-base';
import homeApp from './src/homeApp';
import slotsApp from './src/slotsApp';
import { addApp, addExternalRoute } from './src/utils';

{% if get_frontend_app("authn") %}
import { authnApp } from '@openedx/frontend-app-authn';
{% endif %}

{% if get_frontend_app("learner-dashboard") %}
import { learnerDashboardApp } from '@openedx/frontend-app-learner-dashboard';
{% endif %}

{{ patch("site-config-imports") }}
{{ patch("site-config-imports-production") }}

import './src/site.scss';

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
    homeApp,
    slotsApp,
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

{{ patch("site-config") }}
{{ patch("site-config-production") }}

export default siteConfig;
