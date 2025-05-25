<script lang="ts">
	// Internal Components
	import ConfigureGlycosylation from './Attach Glycans/ConfigureGlycosylation.svelte';
	import UploadGlycans from './Attach Glycans/UploadGlycans.svelte';
</script>

<div class="ag:flex-row flex flex-col content-stretch gap-4">
	<UploadGlycans />
	<hr class="hr ag:hidden" />
	<span class="vr ag:block hidden h-auto"></span>
	<ConfigureGlycosylation />
</div>
