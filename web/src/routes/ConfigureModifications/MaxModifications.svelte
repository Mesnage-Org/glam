<script lang="ts">
	let { value = $bindable() } = $props();

	import { Switch } from '@skeletonlabs/skeleton-svelte';

	let checked = $state(value === null ? false : true);

	function onCheckedChange(e) {
		checked = e.checked;
		if (checked) {
			value = 1;
		} else {
			value = null;
		}
	}
</script>

<label class="label flex items-center justify-between">
	<span class="text-nowrap">Limit Modifications Per Peptide</span>
	<Switch {checked} {onCheckedChange} />
</label>
{#if checked}
	<input class="input" type="number" min="1" bind:value />
{/if}
