<script lang="ts">
	import { getParameters } from '$lib/state.svelte';
	import FileDropzone from '../Shared Components/FileDropzone.svelte';

	let parameters = getParameters();
</script>

<div class="flex w-90 flex-col gap-2">
	<h4 class="h4">Upload Glycans</h4>
	<FileDropzone
		subtext="Upload a glycan database file (.csv)"
		accept="text/csv"
		onFileAccept={(t: string) => (parameters.glycans = t)}
	/>
</div>
