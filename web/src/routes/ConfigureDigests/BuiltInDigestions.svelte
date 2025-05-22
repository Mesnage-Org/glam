<script lang="ts">
	import { getInitData, getParameters } from '$lib/state.svelte';
	import { ProgressRing } from '@skeletonlabs/skeleton-svelte';

	let initData = getInitData();
	let digestSettings = getParameters().digestSettings;

	let value = $state([]);

	function onchange() {
		const regex = value.map((name) => initData.digestions!.get(name)).join('|');
		digestSettings.regex = regex;
	}
</script>

{#if initData.digestions === undefined}
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
		{#each initData.digestions.keys() as name (name)}
			<option value={name}>{name}</option>
		{/each}
	</select>
{/if}
