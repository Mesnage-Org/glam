<script lang="ts">
	// FIXME: Remove `onChange`
	let { onChange, digestions } = $props();

	// External Components
	import { ProgressRing } from '@skeletonlabs/skeleton-svelte';

	// Internal Components
	import AdvancedOptions from './AdvancedOptions.svelte';
	import MissedCleavages from './DigestSettings/MissedCleavages.svelte';
	import PeptideLength from './DigestSettings/PeptideLength.svelte';
	import SemiSpecific from './DigestSettings/SemiSpecific.svelte';

	let selectedDigests = $state([]);
	class DigestSettings {
		regex: string = $derived(selectedDigests.map((n) => digestions()[n]).join('|'));
		missedCleavages: number = $state(0);
		minLength: number | null = $state(null);
		maxLength: number | null = $state(null);
		semiEnzymatic: boolean = $state(false);
	}
	let digestSettings = new DigestSettings();
</script>

<form class="mx-auto flex w-full max-w-md flex-col items-center gap-4">
	<AdvancedOptions>
		<MissedCleavages bind:value={digestSettings.missedCleavages} />
		<hr class="border-surface-200-800" />
		<PeptideLength type="Minimum" bind:value={digestSettings.minLength} />
		<hr class="border-surface-200-800" />
		<PeptideLength type="Maximum" bind:value={digestSettings.maxLength} />
		<hr class="border-surface-200-800" />
		<SemiSpecific bind:value={digestSettings.semiEnzymatic} />
	</AdvancedOptions>
</form>
