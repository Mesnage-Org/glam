<script lang="ts">
	let { value = $bindable() } = $props();

	import { Switch } from '@skeletonlabs/skeleton-svelte';
</script>

<label class="label flex items-center justify-between">
	<span class="text-nowrap">Semi-Specific Cleavage</span>
	<Switch checked={value} onCheckedChange={(e) => value = e.checked} />
</label>
