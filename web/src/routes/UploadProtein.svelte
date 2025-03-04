<script lang="ts">
	import { getParameters } from '$lib/state.svelte';
	import FileDropzone from './FileDropzone.svelte';

	let parameters = getParameters();
</script>

<FileDropzone
	subtext="Upload a protein-containing FASTA file"
	accept={{ 'text/x-fasta': ['.fasta', '.fas', '.fa', '.faa', '.mpfa'] }}
	onFileAccept={(t: string) => (parameters.proteinFasta = t)}
/>
