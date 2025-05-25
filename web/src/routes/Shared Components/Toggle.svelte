<script lang="ts">
	let { label, value = $bindable() } = $props();

	import { Switch } from '@skeletonlabs/skeleton-svelte';
</script>

<label class="label flex items-center justify-between">
	<span class="text-nowrap">{label}</span>
	<Switch checked={value} onCheckedChange={(e) => (value = e.checked)} />
</label>
