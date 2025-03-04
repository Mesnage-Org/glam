<script lang="ts">
	import { onMount } from 'svelte';
	import Glam from '$lib/glam.ts?worker';
	import { InitData, Parameters, setInitData, setParameters } from '$lib/state.svelte';
	import fileDownload from 'js-file-download';

	import { Progress } from '@skeletonlabs/skeleton-svelte';

	// Internal Components
	import FileDropzone from './FileDropzone.svelte';
	import ConfigureDigests from './ConfigureDigests.svelte';
	import ConfigureGlycosylation from './ConfigureGlycosylation.svelte';
	import ConfigureModifications from './ConfigureModifications.svelte';
	import Stepper from './Stepper.svelte';
	import UploadProtein from './UploadProtein.svelte';
	import UploadGlycans from './UploadGlycans.svelte';

	let initData: InitData = new InitData();
	let parameters: Parameters = new Parameters();

	setInitData(initData);
	setParameters(parameters);

	let glam: Worker;
	let glamBusy = $state(true);

	onMount(() => {
		glam = new Glam();
		glam.onmessage = ({ data: msg }) => {
			switch (msg.type) {
				case 'Ready':
					for (const key of Object.keys(msg.initData)) {
						initData[key] = new Map(Object.entries(msg.initData[key]));
					}
					break;
				case 'Result':
					fileDownload(msg.blob, msg.filename);
					break;
			}
			glamBusy = false;
		};
	});

	$inspect(initData.digestions, initData.glycosylationMotifs, initData.modifications);

	$inspect(
		parameters.proteinFasta,
		parameters.digestSettings.regex,
		parameters.digestSettings.missedCleavages,
		parameters.digestSettings.minLength,
		parameters.digestSettings.maxLength,
		parameters.digestSettings.semiEnzymatic,
		parameters.glycanCsv,
		parameters.glycosylationSettings.regex,
		parameters.glycosylationSettings.allPeptides,
		parameters.modificationSettings.modifications,
		parameters.modificationSettings.maxModifications
	);

	let isReady = $derived(
		parameters.proteinFasta !== undefined && parameters.glycanCsv !== undefined && !glamBusy
	);

	function onFinish() {
		glam.postMessage(JSON.stringify(parameters));
		glamBusy = true;
	}

	// Step Components
	const steps = [
		{
			title: 'Upload Protein',
			component: UploadProtein
		},
		{
			title: 'Specify Digests',
			component: ConfigureDigests
		},
		{
			title: 'Upload Glycans',
			component: UploadGlycans
		},
		{
			title: 'Specify Glycosylation Motifs',
			component: ConfigureGlycosylation
		},
		{
			title: 'Specify Modifications',
			component: ConfigureModifications
		}
	];
</script>

<article
	class="w-max-[80%] card border-surface-200-800 preset-filled-surface-100-900 flex w-96 flex-col gap-4 border-2 p-4 text-center"
>
	<Stepper {steps} {isReady} {onFinish} />
	{#if glamBusy}
		<Progress value={null} />
	{/if}
</article>
