<script lang="ts">
	// Internal Components
	import ConfigureDigests from './Generate Peptides/ConfigureDigests.svelte';
	import ConfigureModifications from './Generate Peptides/ConfigureModifications.svelte';
	import UploadProtein from './Generate Peptides/UploadProtein.svelte';
</script>

<div class="gp:flex-row flex flex-col content-stretch gap-4">
	<UploadProtein />
	<hr class="hr gp:hidden" />
	<span class="vr gp:block hidden h-auto"></span>
	<ConfigureDigests />
	<hr class="hr gp:hidden" />
	<span class="vr gp:block hidden h-auto"></span>
	<ConfigureModifications />
</div>
