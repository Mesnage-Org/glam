<script lang="ts">
	import { getParameters } from '$lib/state.svelte';

	// External Components
	import { Tabs } from '@skeletonlabs/skeleton-svelte';

	// Internal Components
	import AdvancedOptions from '../Shared Components/AdvancedOptions.svelte';
	import OptionalCount from '../Shared Components/OptionalCount.svelte';
	import BuiltInModifications from './ConfigureModifications/BuiltInModifications.svelte';
	import CustomModifications from './ConfigureModifications/CustomModifications.svelte';

	let modificationSettings = getParameters().modificationSettings;

	let tab = $state('builtin');
</script>

<div class="flex w-80 flex-col gap-2">
	<h4 class="h4">Specify Modifications</h4>
	<form class="mx-auto flex w-full max-w-md flex-col items-center gap-4">
		<Tabs value={tab} onValueChange={(e) => (tab = e.value)} fluid>
			{#snippet list()}
				<Tabs.Control value="builtin">Built-In</Tabs.Control>
				<Tabs.Control value="custom">Custom</Tabs.Control>
			{/snippet}
			{#snippet content()}
				<Tabs.Panel value="builtin">
					<BuiltInModifications />
				</Tabs.Panel>
				<Tabs.Panel value="custom">
					<CustomModifications />
				</Tabs.Panel>
			{/snippet}
		</Tabs>
		<AdvancedOptions>
			<OptionalCount
				label="Maximum Modification Count"
				bind:value={modificationSettings.maxModifications}
			/>
		</AdvancedOptions>
	</form>
</div>
