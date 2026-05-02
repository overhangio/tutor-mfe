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

{% if get_frontend_compat_slots() %}
import {
  createLegacyPluginApp,
  defaultSlotMap,
  defaultWidgetMap,
} from '@openedx/frontend-base-compat';
import envConfig, { slotCompatMap, widgetCompatMap } from './src/env.config.compat.jsx';
{% endif %}

{{ patch("mfe-site-config-imports") }}
{{ patch("mfe-site-config-imports-development") }}

import '@openedx/frontend-base/shell/style';
import '@edx/brand/core.min.css';
import '@edx/brand/light.min.css';

const siteConfig: SiteConfig = {
  siteId: 'tutor-site',
  siteName: {{ PLATFORM_NAME | tojson }},
  baseUrl: '{{ "https" if ENABLE_HTTPS else "http" }}://{{ MFE_HOST }}:{{ MFE_SITE_PORT }}',
  lmsBaseUrl: '{{ "https" if ENABLE_HTTPS else "http" }}://{{ LMS_HOST }}:8000',
  loginUrl: '{{ "https" if ENABLE_HTTPS else "http" }}://{{ LMS_HOST }}:8000/login',
  logoutUrl: '{{ "https" if ENABLE_HTTPS else "http" }}://{{ LMS_HOST }}:8000/logout',

  environment: EnvironmentTypes.DEVELOPMENT,
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

{% if get_frontend_compat_slots() %}
addApp(siteConfig, createLegacyPluginApp({
  appId: 'io.edly.frontend.app.compat',
  envConfig,
  slotMap: { ...defaultSlotMap, ...slotCompatMap },
  widgetMap: { ...defaultWidgetMap, ...widgetCompatMap },
}));
{% endif %}

{{ patch("mfe-site-config") }}
{{ patch("mfe-site-config-development") }}

export default siteConfig;
