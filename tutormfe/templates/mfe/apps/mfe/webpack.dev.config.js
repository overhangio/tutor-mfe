const { merge } = require('webpack-merge');

const baseDevConfig = require('@edx/frontend-build/config/webpack.dev.config.js');

module.exports = merge(baseDevConfig, {
  // This configuration needs to be defined here, because CLI
  // arguments are ignored by the "npm run start" command
  devServer: {
    // We will have to make changes to thix config in later releases of webpack dev devServer
    // https://github.com/webpack/webpack-dev-server/blob/master/migration-v4.md
    allowedHosts: 'all',
  },
})

{{ patch("mfe-webpack-dev-config") }}
