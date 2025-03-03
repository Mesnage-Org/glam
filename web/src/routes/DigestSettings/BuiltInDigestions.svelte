<script lang="ts">
	let { value = $bindable() } = $props();
	let selectedDigests = $state([]);

	function selectionUpdated() {
		onChange(digestSettings.regex);
	}
</script>

{#if digestions() === undefined}
	<option>
		<ProgressRing
			value={null}
			size="size-14"
			meterStroke="stroke-tertiary-600-400"
			trackStroke="stroke-tertiary-50-950"
		/>
	</option>
{:else}
	<select
		class="select rounded-container overflow-y-auto"
		multiple
		bind:value={selectedDigests}
		onchange={selectionUpdated}
	>
		{#each Object.keys(digestions()) as name}
			<option value={name}>{name}</option>
		{/each}
	</select>
{/if}
