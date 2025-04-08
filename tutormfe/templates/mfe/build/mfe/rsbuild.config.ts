// Install dependencies:
//
//     npm install --no-save @rsbuild/core @rsbuild/plugin-react @rsbuild/plugin-svgr @rsbuild/plugin-sass @rsdoctor/rspack-plugin
//
// Build with:
//
//     rsbuild build
//
// Develop with:
//
//     rsbuild
//
// Troubleshoot with:
//
//     RSDOCTOR=true rsbuild build

import path from 'path';
import fs from 'fs';
import { defineConfig } from '@rsbuild/core';
import { pluginReact } from '@rsbuild/plugin-react';
import { pluginSvgr } from '@rsbuild/plugin-svgr';
import { pluginSass } from '@rsbuild/plugin-sass';
import { loadEnv } from '@rsbuild/core';

// Load environment variables
// https://rsbuild.dev/api/javascript-api/core#loadenv
const currentDir = process.cwd();
const parsedEnv = loadEnv({ mode: 'production' }).parsed;
const parsedEnvDev = loadEnv({ mode: 'development' }).parsed;
const appName = parsedEnv.APP_ID || path.basename(currentDir).replace('frontend-app-', '');
const publicPath = parsedEnv.PUBLIC_PATH || '/' + appName + '/';
const dev = parsedEnv.NODE_ENV === 'development';
const prod = !dev;
parsedEnv.APP_ID = appName;
parsedEnv.PUBLIC_PATH = publicPath;
parsedEnv.MFE_CONFIG_API_URL = prod ? '/api/mfe_config/v1' : 'http://local.openedx.io:8000/api/mfe_config/v1';

// Load env.config.(js|jsx)
var envConfigPath = '';
try {
    await import('@openedx/frontend-plugin-framework');
    if (fs.existsSync(path.resolve(currentDir, './env.config.jsx'))) {
        envConfigPath = path.resolve(currentDir, './env.config.jsx');
    } else if (fs.existsSync(path.resolve(currentDir, './env.config.js'))) {
        envConfigPath = path.resolve(currentDir, './env.config.js');
    }
} catch {
    // FPF is not available, we don't try to load env.config.js
}

const config = defineConfig({
    html: {
        template: './public/index.html',
    },
    output: {
        // Flat directory
        // TODO do we want a flat directory?
        // distPath: {
        //     js: '',
        //     css: '',
        // },
        sourceMap: {
            js: prod ? 'source-map' : 'eval',
            css: true,
        }
    },
    performance: {
        // We enable caching everywhere, even if it's unnecessary in some places. The
        // negative impact on performance should be minor.
        buildCache: true,
    },
    server: {
        base: publicPath,
        // Redirect all get requests to index.html
        // https://rsbuild.dev/config/server/history-api-fallback
        historyApiFallback: true,
        port: parseInt(parsedEnvDev.PORT),
    },
    source: {
        define: {
            // This is explicitly recommended against, but this is how MFEs are built
            // https://rsbuild.dev/guide/advanced/env-vars#processenv-replacement
            'process.env': JSON.stringify(parsedEnv),
        },
        transformImport: [
            // https://rsbuild.dev/config/source/transform-import#import-lodash-on-demand
            {
                libraryName: 'lodash',
                customName: 'lodash/{' + '{ member }' + '}',
            },
            {
                libraryName: '@fortawesome/free-brands-svg-icons',
                customName: '@fortawesome/free-brands-svg-icons/{' + '{ member }' + '}',
                transformToDefaultImport: false,
            },
            {
                libraryName: '@fortawesome/free-regular-svg-icons',
                customName: '@fortawesome/free-regular-svg-icons/{' + '{ member }' + '}',
                transformToDefaultImport: false,
            },
            {
                libraryName: '@fortawesome/free-solid-svg-icons',
                customName: '@fortawesome/free-solid-svg-icons/{' + '{ member }' + '}',
                transformToDefaultImport: false,
            },
        ],
    },
    plugins: [
        // https://rsbuild.dev/plugins/list/plugin-react
        pluginReact(),
        // https://rsbuild.dev/plugins/list/plugin-svgr#mixedimport
        pluginSvgr({
            mixedImport: true,
            svgrOptions: {
                exportType: 'named',
            },
        }),
        // https://rsbuild.dev/plugins/list/plugin-sass
        pluginSass({
            sassLoaderOptions: {
                sassOptions: {
                    silenceDeprecations: ['abs-percent', 'color-functions', 'import', 'mixed-decls', 'global-builtin', 'legacy-js-api'],
                },
            },
        }),
    ],
    resolve: {
        alias: {
            'env.config': envConfigPath || false,
        }
    }
});

///////////////////////
// MFE-specific changes
///////////////////////

// This is horrible but we don't have a choice
if (appName == 'authoring') {
    config.resolve!.alias!['CourseAuthoring'] = path.resolve(currentDir, 'src/');
} else if (appName == 'communications') {
    // config.resolve!.alias![''] = './src';
    config.resolve!.alias!['@src'] = path.resolve(currentDir, 'src');
} else if (appName == 'gradebook') {
    // config.resolve!.alias![''] = './src';
    config.resolve!.alias!['@src'] = path.resolve(currentDir, 'src');
} else if (appName == 'learner-dashboard') {
    // config.resolve!.alias![''] = './src';
    config.resolve!.alias!['@src'] = path.resolve(currentDir, 'src');
} else if (appName === 'learning') {
    config.resolve!.alias!['@src'] = path.resolve(currentDir, 'src');
} else if (appName == 'ora-grading') {
    // config.resolve!.alias![''] = './src';
    config.resolve!.alias!['@src'] = path.resolve(currentDir, 'src');
}

export default config;
