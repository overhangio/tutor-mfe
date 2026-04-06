import { App, getUrlByRouteRole } from '@openedx/frontend-base';
import { redirect } from 'react-router';

const homeApp: App = {
  appId: 'home',
  routes: [{
    path: '/',
    loader: () => {
      const homeUrl = getUrlByRouteRole('{{ MFE_SITE_HOME }}');
      if (homeUrl) {
        return redirect(homeUrl);
      }
      throw new Response('Not Found', { status: 404 });
    },
  }],
};

export default homeApp;
