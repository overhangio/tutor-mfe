const fs = require('fs');
const path = require('path');

const baseProdConfig = (
  fs.existsSync('./webpack.prod.config.js')
    ? require('./webpack.prod.config.js')
    : require('@openedx/frontend-build/config/webpack.prod.config.js')
);

{% if not MFE_REMOVE_WEBPACK_BUILD_CACHE %}
// This speeds up subsequent builds when Docker layer cache is reused.
baseProdConfig.cache = {
  type: 'filesystem',
  cacheDirectory: path.resolve(__dirname, '.cache'),
};
{% endif %}

// Disable plugins that are not required in Tutor production builds.
baseProdConfig.plugins = (baseProdConfig.plugins || [])
  .filter((plugin) => plugin?.constructor?.name !== 'NewRelicPlugin')
  .filter((plugin) => plugin?.constructor?.name !== 'HtmlWebpackNewRelicPlugin')
  .filter((plugin) => plugin?.constructor?.name !== 'BundleAnalyzerPlugin');

// Source maps increase output size significantly and are unnecessary by default.
baseProdConfig.devtool = false;

module.exports = baseProdConfig;

{{ patch("mfe-webpack-prod-config") }}
