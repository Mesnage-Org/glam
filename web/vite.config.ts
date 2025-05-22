import tailwindcss from '@tailwindcss/vite';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit(), tailwindcss()],
	worker: {
		plugins: () => [sveltekit()],
		format: 'es'
	},
	esbuild: {
		supported: {
			'top-level-await': true
		}
	}
});
