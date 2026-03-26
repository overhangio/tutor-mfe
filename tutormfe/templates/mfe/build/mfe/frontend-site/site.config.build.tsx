import { EnvironmentTypes, SiteConfig, footerApp, headerApp, shellApp } from '@openedx/frontend-base';
{%- for app_name, app_attrs in iter_frontend_apps() %}
{%- set camel_case_name = app_name.split('-') | map('title') | list %}
{%- set camel_case_name = camel_case_name[0].lower() + (camel_case_name[1:] | join('')) %}
import { {{ camel_case_name }}App } from '@openedx/frontend-app-{{ app_name }}';
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
{%- set camel_case_name = app_name.split('-') | map('title') | list %}
{%- set camel_case_name = camel_case_name[0].lower() + (camel_case_name[1:] | join('')) %}
    {{ camel_case_name }}App,
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
