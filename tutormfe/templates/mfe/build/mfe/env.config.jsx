{{- patch("mfe-env-config-static-imports") }}
{{- patch("mfe-env-config-head") }}

async function getConfig () {
  let config = {};

  try {
    /* We can't assume FPF exists, as it's not declared as a dependency in all
     * MFEs, so we import it dynamically. In addition, for dynamic imports to
     * work with Webpack all of the code that actually uses the imported module
     * needs to be inside the `try{}` block.
     */
    const { DIRECT_PLUGIN, PLUGIN_OPERATIONS } = await import('@openedx/frontend-plugin-framework');
    {{- patch("mfe-env-config-dynamic-imports") }}

    config = {
      pluginSlots: {
        {%- for slot_name in iter_slots() %}
        {%- if patch("mfe-env-config-plugin-{}".format(slot_name)) %}
        {{ slot_name }}: {
          keepDefault: true,
          plugins: [
            {{- patch("mfe-env-config-plugin-{}".format(slot_name)) }}
          ]
        },
        {%- endif %}
        {%- endfor %}
      }
    };

    {%- for app_name, app in iter_mfes() %}
    if (process.env.npm_package_name == '@edx/frontend-app-{{ app_name }}') {
      {%- if patch("mfe-env-config-dynamic-imports-{}".format(app_name)) %}
      {{- patch("mfe-env-config-dynamic-imports-{}".format(app_name)) }}
      {%- endif %}

      {%- for slot_name in iter_slots() %}
      {%- if patch("mfe-env-config-plugin-{}-{}".format(app_name, slot_name)) %}
      config.pluginSlots.{{ slot_name }}.plugins.push(
        {{- patch("mfe-env-config-plugin-{}-{}".format(app_name, slot_name)) }}
      );
      {%- endif %}
      {%- endfor %}
    }
    {%- endfor %}

    {{- patch("mfe-env-config-tail") }}
  } catch { }

  return config;
}

export default getConfig;
