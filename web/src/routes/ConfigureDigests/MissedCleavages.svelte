<script lang="ts">
	let { value = $bindable() } = $props();
</script>

<label class="label flex items-center gap-4">
	<span class="text-nowrap">Missed Cleavages</span>
	<input class="input" type="number" min="0" bind:value />
</label>
