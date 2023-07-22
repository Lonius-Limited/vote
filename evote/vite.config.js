import path from 'path';
import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react'
import proxyOptions from './proxyOptions';
// const pkg = require('./package.json');

// https://vitejs.dev/config/
export default defineConfig(({ command, mode }) => {
	const env = loadEnv(mode, process.cwd(), '')
	return {
		plugins: [react()],
		define: { 'process.env': env },
		server: {
			port: 8080,
			proxy: proxyOptions
		},
		resolve: {
			alias: {
				'@': path.resolve(__dirname, 'src')
			},
			extensions: ['.mjs', '.js', '.ts', '.jsx', '.tsx', '.json']
		},
		build: {
			outDir: '../vote/public/evote',
			emptyOutDir: true,
			target: 'es2015',
			rollupOptions: {
				// external: ["evote/node_modules/"]
				external: [
					"./evote/node_modules/react",
					"./evote/node_modules/react/jsx-runtime/",
					// "react/jsx-runtime",
					"./evote/node_modules/frappe-react-sdk/",
					"./evote/node_modules/antd/*",
					"./evote/node_modules/@uidotdev/usehooks/"
				], output: {
					globals: {
						'react': 'react',
						//   'react-dom': 'ReactDOM',
						'react/jsx-runtime': 'react/jsx-runtime',
					},
				},

			}
		},

	}
});
// export default defineConfig(({ command, mode }) => {
//     // Load env file based on `mode` in the current working directory.
//     // Set the third parameter to '' to load all env regardless of the `VITE_` prefix.
//     const env = loadEnv(mode, process.cwd(), '')
//     return {
//         // vite config
//         plugins: [react()],
//         define: {
//             'process.env': env,
//         },
//         server: {
//             host: "0.0.0.0"
//         }
//     }
// })