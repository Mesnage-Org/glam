<script lang="ts">
	let { children } = $props();

	// External Components
	import { Accordion } from '@skeletonlabs/skeleton-svelte';

	// Icons
	import { Settings2 } from 'lucide-svelte';

	let value: string[] = $state([]);
</script>

<Accordion {value} onValueChange={(e) => (value = e.value)} collapsible>
	<Accordion.Item value="open">
		{#snippet lead()}<Settings2 size={24} />{/snippet}
		{#snippet control()}Advanced Options{/snippet}
		{#snippet panel()}
			<div class="flex flex-col gap-4">
				{@render children()}
			</div>
		{/snippet}
	</Accordion.Item>
</Accordion>
