<script lang="ts">
	import { getInitData, getParameters } from '$lib/state.svelte';

	import { ProgressRing } from '@skeletonlabs/skeleton-svelte';

	let value = $state([]);

	let initData = getInitData();
	let modificationSettings = getParameters().modificationSettings;

	function onchange() {
		const mods = value.map((name) => initData.modifications!.get(name)!);
		modificationSettings.modifications = mods;
	}
</script>

{#if initData.modifications === undefined}
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
		{#each initData.modifications.keys() as name (name)}
			<option value={name}>{name}</option>
		{/each}
	</select>
{/if}
