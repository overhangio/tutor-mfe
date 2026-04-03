import { App, WidgetOperationTypes } from '@openedx/frontend-base';

{{- patch("frontend-slots-env-config-buildtime-imports") }}

const slotsApp: App = {
  appId: 'slots',
  slots: [
    {%- for slot_name, slot_config in iter_frontend_slots() %}
    {{ slot_config }},
    {%- endfor %}
  ]
};

export default slotsApp;
