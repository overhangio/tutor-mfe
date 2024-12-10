{{- patch("mfe-env-config-buildtime-imports") }}

function addPlugins(config, slot_name, plugins) {
  if (slot_name in config.pluginSlots === false) {
    config.pluginSlots[slot_name] = {
      keepDefault: true,
      plugins: []
    };
  }

  config.pluginSlots[slot_name].plugins.push(...plugins);
}

{{- patch("mfe-env-config-buildtime-definitions") }}

async function setConfig () {
  let config = {
    pluginSlots: {}
  };

  try {
    /* We can't assume FPF exists, as it's not declared as a dependency in all
     * MFEs, so we import it dynamically. In addition, for dynamic imports to
     * work with Webpack all of the code that actually uses the imported module
     * needs to be inside the `try{}` block.
     */
    const { DIRECT_PLUGIN, PLUGIN_OPERATIONS } = await import('@openedx/frontend-plugin-framework');

    {{- patch("mfe-env-config-runtime-definitions") }}

    {%- for slot_name, plugin_config in iter_plugin_slots("all") %}
    addPlugins(config, '{{ slot_name }}', [{{ plugin_config }}]);
    {%- endfor %}

    {%- for app_name, _ in iter_mfes() %}
    if (process.env.APP_ID == '{{ app_name }}') {
      {{- patch("mfe-env-config-runtime-definitions-{}".format(app_name)) }}

      {%- for slot_name, plugin_config in iter_plugin_slots(app_name) %}
      addPlugins(config, '{{ slot_name }}', [{{ plugin_config }}]);
      {%- endfor %}
    }
    {%- endfor %}

    {{- patch("mfe-env-config-runtime-final") }}
  } catch { }

  return config;
}

export default setConfig;
