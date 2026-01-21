module.exports = {
  localModules: [
  {%- if mfe_plugin_mounts is defined %}
    {%- for mount in mfe_plugin_mounts(MOUNTS) %}
    {
      moduleName: '{{ mount.module_name }}',
      dir: '{{ mount.mounted_path }}'
    },
    {% endfor -%}
  {% endif -%}
  ],
};
