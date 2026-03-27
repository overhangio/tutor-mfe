import { EnvironmentTypes, SiteConfig, footerApp, headerApp, shellApp } from '@openedx/frontend-base';
{%- for app_name, app_attrs in iter_frontend_apps() %}
{%- set components = app_attrs.get('appEntryPoints', {}).get('components', []) %}
{% if components %}
import { {{ components | join(', ') }} } from '{{ app_attrs.get('appEntryPoints', {}).get('packageName', app_name) }}';
{% endif %}
{%- endfor %}
import homeApp from './src/homeApp';


import './src/site.scss';

const siteConfig: SiteConfig = {
  siteId: 'frontend-template-site',
  siteName: 'Frontend Template Site',
  baseUrl: '{{ "https" if ENABLE_HTTPS else "http" }}://{{ MFE_HOST }}:8080',
  lmsBaseUrl: '{{ "https" if ENABLE_HTTPS else "http" }}://{{ LMS_HOST }}:8000',
  loginUrl: '{{ "https" if ENABLE_HTTPS else "http" }}://{{ LMS_HOST }}:8000/login',
  logoutUrl: '{{ "https" if ENABLE_HTTPS else "http" }}://{{ LMS_HOST }}:8000/logout',

  environment: EnvironmentTypes.PRODUCTION,
  apps: [
    shellApp,
    headerApp,
    footerApp,
{%- for app_name, app_attrs in iter_frontend_apps() %}
{%- set components = app_attrs.get('appEntryPoints', {}).get('components', []) %}
{%- if components %}
    {{ components | join(',') }},
{%- endif %}
{%- endfor %}
    homeApp,
  ],
  externalRoutes: [
    {
      role: 'org.openedx.frontend.role.profile',
      url: '{{ "https" if ENABLE_HTTPS else "http" }}://{{ MFE_HOST }}/profile/'
    },
    {
      role: 'org.openedx.frontend.role.account',
      url: '{{ "https" if ENABLE_HTTPS else "http" }}://{{ MFE_HOST }}/account/'
    },
    {
      role: 'org.openedx.frontend.role.logout',
      url: '{{ "https" if ENABLE_HTTPS else "http" }}://{{ LMS_HOST }}/logout'
    },
  ],

  accessTokenCookieName: 'edx-jwt-cookie-header-payload',
};

export default siteConfig;
