<script lang="ts">
	import { getInitData, getParameters } from '$lib/state.svelte';

	import { ProgressRing } from '@skeletonlabs/skeleton-svelte';

	let value = $state([]);

	let initData = getInitData();
	let glycosylationSettings = getParameters().glycosylationSettings;

	function onchange() {
		const regex = value.map((name) => initData.glycosylationMotifs!.get(name)).join('|');
		glycosylationSettings.motif = regex;
	}
</script>

{#if initData.glycosylationMotifs === undefined}
	<div class="flex justify-center">
		<ProgressRing
			value={null}
			size="size-14"
			meterStroke="stroke-tertiary-600-400"
			trackStroke="stroke-tertiary-50-950"
		/>
	</div>
{:else}
	<select class="select rounded-container overflow-y-auto" multiple bind:value {onchange}>
		{#each initData.glycosylationMotifs.keys() as name (name)}
			<option value={name}>{name}</option>
		{/each}
	</select>
{/if}
