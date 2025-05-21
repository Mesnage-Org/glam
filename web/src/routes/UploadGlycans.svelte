<script lang="ts">
	import { getParameters } from '$lib/state.svelte';
	import FileDropzone from './FileDropzone.svelte';

	let parameters = getParameters();
</script>

<FileDropzone
	subtext="Upload a glycan database file (.csv)"
	accept="text/csv"
	onFileAccept={(t: string) => (parameters.glycans = t)}
/>
