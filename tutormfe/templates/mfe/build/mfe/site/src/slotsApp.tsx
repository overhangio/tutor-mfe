import { App } from '@openedx/frontend-base';
import { addSlot } from './utils';

{{- patch("mfe-site-slots-imports") }}

const slotsApp: App = {
  appId: 'slots',
};

{%- for slot_operation in iter_frontend_slots() %}
addSlot(slotsApp, {{ slot_operation }});
{%- endfor %}

{{- patch("mfe-site-slots") }}

export default slotsApp;
