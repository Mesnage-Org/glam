<script lang="ts">
	import { getInitData, getParameters } from '$lib/state.svelte';

	// External Components
	import { Tabs } from '@skeletonlabs/skeleton-svelte';

	// Internal Components
	import AdvancedOptions from './AdvancedOptions.svelte';
	import MissedCleavages from './ConfigureDigests/MissedCleavages.svelte';
	import PeptideLength from './ConfigureDigests/PeptideLength.svelte';
	import SemiSpecific from './ConfigureDigests/SemiSpecific.svelte';
	import BuiltInDigestions from './ConfigureDigests/BuiltInDigestions.svelte';

	let digestSettings = getParameters().digestSettings;

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
				<BuiltInDigestions />
			</Tabs.Panel>
			<Tabs.Panel value="custom">
				<input class="input" type="text" bind:value={digestSettings.regex} />
			</Tabs.Panel>
		{/snippet}
	</Tabs>
	<AdvancedOptions>
		<MissedCleavages bind:value={digestSettings.missedCleavages} />
		<hr class="border-surface-200-800" />
		<PeptideLength type="Minimum" bind:value={digestSettings.minLength} />
		<hr class="border-surface-200-800" />
		<PeptideLength type="Maximum" bind:value={digestSettings.maxLength} />
		<hr class="border-surface-200-800" />
		<SemiSpecific bind:value={digestSettings.semiEnzymatic} />
	</AdvancedOptions>
</form>
