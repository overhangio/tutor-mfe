import { App, getUrlByRouteRole } from '@openedx/frontend-base';
import { redirect } from 'react-router';

{%- set defaultSite = get_frontend_sites().get('default', {}) %}
const homeApp: App = {
  appId: 'home',
  routes: [{
    path: '/',
    loader: () => {
      const dashboardUrl = getUrlByRouteRole('{{ defaultSite.get('siteConfig', {}).get('redirectRoleId', '') }}');
      if (dashboardUrl) {
        return redirect(dashboardUrl);
      }
      throw new Response('Not Found', { status: 404 });
    },
  }],
};

export default homeApp;
