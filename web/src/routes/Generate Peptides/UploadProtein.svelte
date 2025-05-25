<script lang="ts">
	import { getParameters } from '$lib/state.svelte';
	import FileDropzone from '../Shared Components/FileDropzone.svelte';

	let parameters = getParameters();
</script>

<div class="flex w-80 flex-col gap-2">
	<h4 class="h4">Upload Protein</h4>
	<FileDropzone
		subtext="Upload a protein-containing FASTA file"
		accept={{ 'text/x-fasta': ['.fasta', '.fas', '.fa', '.faa', '.mpfa'] }}
		onFileAccept={(t: string) => (parameters.fasta = t)}
	/>
</div>
