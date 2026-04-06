import { App, ExternalRoute, SiteConfig, SlotOperation } from '@openedx/frontend-base';

export function addApp(config: SiteConfig, app: App) {
  config.apps ??= [];
  config.apps.push(app);
}

export function addExternalRoute(config: SiteConfig, route: ExternalRoute) {
  config.externalRoutes ??= [];
  config.externalRoutes.push(route);
}

export function addSlot(app: App, slot: SlotOperation) {
  app.slots = app.slots ?? [];
  app.slots.push(slot);
}
