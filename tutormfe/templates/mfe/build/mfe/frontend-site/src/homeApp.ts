import { App, getUrlByRouteRole } from '@openedx/frontend-base';
import { redirect } from 'react-router';

const homeApp: App = {
  appId: 'home',
  routes: [{
    path: '/',
    loader: () => {
      const dashboardUrl = getUrlByRouteRole('org.openedx.frontend.role.dashboard');
      if (dashboardUrl) {
        return redirect(dashboardUrl);
      }
      throw new Response('Not Found', { status: 404 });
    },
  }],
};

export default homeApp;
