<script lang="ts">
	import { onMount } from 'svelte';
	import Glam from '$lib/glam.ts?worker';
	import fileDownload from 'js-file-download';

	// Internal Components
	import FileDropzone from './FileDropzone.svelte';
	import DigestSettings from './DigestSettings.svelte';
	import Stepper from './Stepper.svelte';

	let fasta: string | undefined = $state();
	// FIXME: Move this to some object with the glycan sites and modifications
	let digestions = $state();
	let digestRegex = $state('');
	let csv: string | undefined = $state();

	let digest_settings = $state({
		missed_cleavages: 0,
		min_length: null,
		max_length: null,
		semi_enzymatic: false
	});

	let glam: Worker;

	onMount(() => {
		glam = new Glam();
		glam.onmessage = ({ data: msg }) => {
			console.log(msg);
			switch (msg.type) {
				case 'Ready':
					digestions = msg.digestions;
					break;
				case 'Result':
					fileDownload(msg.blob, msg.filename);
					break;
			}
		};
	});

	function runGlam() {
		glam.postMessage({
			fasta,
			digestRegex,
			csv,
			missed_cleavages: digest_settings.missed_cleavages
		});
	}

	// Step Components
	const steps = [
		{
			title: 'Upload Protein',
			component: FileDropzone,
			props: {
				onFileAccept: (text: string) => (fasta = text),
				subtext: 'Upload a protein-containing FASTA file',
				accept: { 'text/x-fasta': ['.fasta', '.fas', '.fa', '.faa', '.mpfa'] }
			}
		},
		{
			title: 'Specify Digests',
			component: DigestSettings,
			props: { onChange: (regex: string) => console.log(regex), digestions: () => digestions }
		},
		{
			title: 'Upload Glycans',
			component: FileDropzone,
			props: {
				onFileAccept: (text: string) => (csv = text),
				subtext: 'Upload a glycan database file (.csv)',
				accept: 'text/csv'
			}
		}
	];
</script>

<article
	class="w-max-[80%] card border-surface-200-800 preset-filled-surface-100-900 w-96 border-2 p-4 text-center"
>
	<Stepper {steps} />
</article>
