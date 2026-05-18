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

{% if get_frontend_compat_mfes() %}
import {
  createLegacyPluginApp,
  defaultRouteMap,
  defaultSlotMap,
  defaultWidgetMap,
} from '@openedx/frontend-base-compat';
{%- for mfe in iter_frontend_compat_mfes() %}
import {{ camelize_mfe_name(mfe) }}EnvConfig from './src/env.config.{{ mfe }}.jsx';
{%- endfor %}

const routeMap = { ...defaultRouteMap, ...{{ get_frontend_route_compat_map() | tojson }} };
const slotMap = { ...defaultSlotMap, ...{{ get_frontend_slot_compat_map() | tojson }} };
const widgetMap = { ...defaultWidgetMap, ...{{ get_frontend_widget_compat_map() | tojson }} };
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
  cmsBaseUrl: '{{ "https" if ENABLE_HTTPS else "http" }}://{{ CMS_HOST }}',
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

{%- for mfe in iter_frontend_compat_mfes() %}
addApp(siteConfig, createLegacyPluginApp({
  appId: 'io.edly.frontend.app.compat.{{ camelize_mfe_name(mfe) }}',
  envConfig: {{ camelize_mfe_name(mfe) }}EnvConfig,
  {%- if mfe != "all" %}
  mfeId: '{{ mfe }}',
  {%- endif %}
  routeMap,
  slotMap,
  widgetMap,
}));
{%- endfor %}

{{ patch("mfe-site-config") }}
{{ patch("mfe-site-config-production") }}

export default siteConfig;
