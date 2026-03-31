import { EnvironmentTypes, SiteConfig, footerApp, headerApp, shellApp } from '@openedx/frontend-base';
{%- for app_name, app_attrs in iter_frontend_apps() %}
{%- set components = app_attrs.get('appEntryPoints', {}).get('components', []) %}
{%- if components %}
import { {{ components | join(', ') }} } from '{{ app_attrs.get('appEntryPoints', {}).get('packageName', app_name) }}';
{%- endif %}
{%- endfor %}
import homeApp from './src/homeApp';


import './src/site.scss';

{%- set defaultSite = get_frontend_sites().get('default', {}) %}
const siteConfig: SiteConfig = {
  siteId: {{defaultSite.get('siteConfig', {}).get('siteId', '"tutor-frontend-site"') | tojson }},
  siteName: {{defaultSite.get('siteConfig', {}).get('siteName', '"Frontend Template Site"') | tojson }},
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
    {%- for route in defaultSite.get('siteConfig', {}).get('externalRoutes', []) %}
    {
      role: '{{ route.role }}',
      url: '{{ 'https' if ENABLE_HTTPS else 'http' }}://{{ MFE_HOST }}{{ route.url }}',
    },
    {%- endfor %}
  ],

  accessTokenCookieName: {{ defaultSite.get('siteConfig', {}).get('accessTokenCookieName', '"edx-jwt-cookie-header-payload"') | tojson }},
};

export default siteConfig;
