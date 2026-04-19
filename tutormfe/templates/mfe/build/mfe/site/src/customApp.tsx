import { App } from '@openedx/frontend-base';
import { addScript, addSlot } from './utils';

{{- patch("mfe-site-custom-app-imports") }}

const customApp: App = {
  appId: 'custom',
};

{{- patch("mfe-site-custom-app-definitions") }}

{%- for slot_operation in iter_frontend_slots() %}
addSlot(customApp, {{ slot_operation }});
{%- endfor %}

{%- for script_loader in iter_external_scripts("site") %}
addScript(customApp, {{ script_loader }});
{%- endfor %}

{%- for script_loader in iter_external_scripts("all") %}
addScript(customApp, {{ script_loader }});
{%- endfor %}

{{- patch("mfe-site-custom-app-final") }}

export default customApp;
