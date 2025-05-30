<script lang="ts">
	import { BookText } from 'lucide-svelte';
	import { base } from '$app/paths';
	import '../app.css';
	import { SiGithub } from '@icons-pack/svelte-simple-icons';
	import CitationModal from './CitationModal.svelte';
	let { children } = $props();
</script>

<!-- Full‐height flex container -->
<div class="flex h-screen flex-col">
	<!-- HEADER: fixed at top of the flex container -->
	<header class="p-4">
		<div class="flex items-center justify-between">
			<span class="text-4xl font-bold">GLAM</span>
			<nav class="flex gap-4">
				<a href="https://mesnage-org.github.io/pgfinder" target="_blank" class="text-lg hover:underline">
					PGFinder
				</a>
				<a href="{base}/docs/glam/index.html" target="_blank">
					<BookText />
				</a>

				<a href="https://github.com/Mesnage-Org/glam" target="_blank">
					<SiGithub />
				</a>
			</nav>
		</div>
	</header>

	<!-- MAIN: grows to fill available space and scrolls internally -->
	<main class="flex h-dvh items-center-safe justify-center-safe overflow-auto">
		{@render children()}
	</main>

	<!-- FOOTER: fixed at bottom of the flex container -->
	<footer class="flex items-center justify-between p-4">
		<CitationModal />
		<p class="text-right text-sm">
			Any issues or suggestions? Please get in touch!<br />
			<a href="mailto:smesnage@sheffield.ac.uk" class="font-semibold hover:underline">
				smesnage@sheffield.ac.uk
			</a>
		</p>
	</footer>
</div>
