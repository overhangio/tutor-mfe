const { merge } = require('webpack-merge');
const fs = require('fs');

const baseDevConfig = (
  fs.existsSync('./webpack.dev.config.js')
    ? require('./webpack.dev.config.js')
    : require('@openedx/frontend-build/config/webpack.dev.config.js')
);

module.exports = merge(baseDevConfig, {
  // This configuration needs to be defined here, because CLI
  // arguments are ignored by the "npm run start" command
  devServer: {
    // We will have to make changes to this config in later releases of webpack dev devServer
    // https://github.com/webpack/webpack-dev-server/blob/master/migration-v4.md
    allowedHosts: 'all',
    proxy: {
      '/api/mfe_config/v1': {
        target: 'http://{{ LMS_HOST }}:8000',
        changeOrigin: true,
      }
    }
  },
})

{{ patch("mfe-webpack-dev-config") }}
