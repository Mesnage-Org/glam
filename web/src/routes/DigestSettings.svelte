<script lang="ts">
	let { onChange, digestions } = $props();

	// Internal Components
	import AdvancedOptions from './AdvancedOptions.svelte';

	let selectedDigests = $state([]);
	class DigestSettings {
		regex: string = $derived(selectedDigests.map((n) => digestions()[n]).join('|'));
		missedCleavages: number = $state(0);
		minLength: number | null = $state(null);
		maxLength: number | null = $state(null);
		semiEnzymatic: boolean = $state(false);
	}
	let digestSettings = new DigestSettings();

	function selectionUpdated() {
		onChange(digestSettings.regex);
	}
</script>

<form class="mx-auto flex w-full max-w-md flex-col items-center gap-4">
	<select
		class="select rounded-container overflow-y-auto"
		multiple
		bind:value={selectedDigests}
		onchange={selectionUpdated}
	>
		{#if digestions() === undefined}
			<option>:(</option>
		{:else}
			{#each Object.keys(digestions()) as name}
				<option value={name}>{name}</option>
			{/each}
		{/if}
	</select>
	<AdvancedOptions>
		<label class="label flex items-center gap-4">
			<span class="text-nowrap">Missed Cleavages</span>
			<input class="input" type="number" min="0" bind:value={digestSettings.missedCleavages} />
		</label>
	</AdvancedOptions>
</form>
