<script lang="ts">
	import { getParameters } from '$lib/state.svelte';

	// External Components
	import { Tabs } from '@skeletonlabs/skeleton-svelte';

	// Internal Components
	import AdvancedOptions from './AdvancedOptions.svelte';
	import AllPeptides from './ConfigureGlycosylation/AllPeptides.svelte';
	import BuiltInMotifs from './ConfigureGlycosylation/BuiltInMotifs.svelte';
	import OptionalCount from './OptionalCount.svelte';

	let glycosylationSettings = getParameters().glycosylationSettings;

	let tab = $state('builtin');
</script>

<form class="mx-auto flex w-full max-w-md flex-col items-center gap-4">
	<Tabs value={tab} onValueChange={(e) => (tab = e.value)} fluid>
		{#snippet list()}
			<Tabs.Control value="builtin">Built-In</Tabs.Control>
			<Tabs.Control value="custom">Custom Regex</Tabs.Control>
		{/snippet}
		{#snippet content()}
			<Tabs.Panel value="builtin">
				<BuiltInMotifs />
			</Tabs.Panel>
			<Tabs.Panel value="custom">
				<input class="input" type="text" bind:value={glycosylationSettings.motif} />
			</Tabs.Panel>
		{/snippet}
	</Tabs>
	<AdvancedOptions>
		<OptionalCount label="Maximum Glycan Count" bind:value={glycosylationSettings.maxGlycans} />
		<hr class="border-surface-200-800" />
		<AllPeptides bind:value={glycosylationSettings.allPeptides} />
	</AdvancedOptions>
</form>
