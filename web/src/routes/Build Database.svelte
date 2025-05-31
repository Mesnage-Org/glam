<script lang="ts">
	let { isReady, onFinish } = $props();
	import { Download, Link } from 'lucide-svelte';
</script>

<div class="flex flex-col content-stretch gap-4">
	<button
		type="button"
		class={[
			'btn preset-tonal-success bd:min-w-124 h-32 w-full min-w-80 space-x-2 rounded-xl text-2xl',
			isReady() && 'hover:preset-filled-success-700-300'
		]}
		onclick={onFinish()}
		disabled={!isReady()}
	>
		<Download size={25} />
		<span>Build Database</span>
	</button>
	<div class="flex items-center gap-4">
		<hr class="hr" />
		<span>Next</span>
		<hr class="hr" />
	</div>
	<a
		href="https://mesnage-org.github.io/pgfinder"
		target="_blank"
		class="btn preset-tonal hover:preset-filled h-32 w-full space-x-2 rounded-xl text-2xl"
	>
		<Link size={25} />
		<span>MS1 Analysis (PGFinder)</span>
	</a>
</div>
