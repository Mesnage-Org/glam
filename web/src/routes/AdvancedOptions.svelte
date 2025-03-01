<script lang="ts">
	let { children } = $props();

	// External Components
	import { Accordion } from '@skeletonlabs/skeleton-svelte';

	// Icons
	import { Settings2 } from 'lucide-svelte';
</script>

<Accordion value={[]} collapsible>
	<Accordion.Item value="open">
		{#snippet lead()}<Settings2 size={24} />{/snippet}
		{#snippet control()}Advanced Options{/snippet}
		{#snippet panel()}
			{@render children()}
		{/snippet}
	</Accordion.Item>
</Accordion>
