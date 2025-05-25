<script lang="ts">
	import { onMount } from 'svelte';
	import Glam from '$lib/glam.ts?worker';
	import { InitData, Parameters, setInitData, setParameters } from '$lib/state.svelte';
	import fileDownload from 'js-file-download';

	// External Components
	import { Progress } from '@skeletonlabs/skeleton-svelte';

	// Internal Components
	import AttachGlycans from './Attach Glycans.svelte';
	import GeneratePeptides from './Generate Peptides.svelte';
	import Stepper from './Stepper.svelte';

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
						// @ts-expect-error need to add a type to `msg` to convince TS that keys will line up here
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
		parameters.fasta,
		parameters.digestSettings.digestion,
		parameters.digestSettings.missedCleavages,
		parameters.digestSettings.minLength,
		parameters.digestSettings.maxLength,
		parameters.digestSettings.semiEnzymatic,
		parameters.glycans,
		parameters.glycosylationSettings.motif,
		parameters.glycosylationSettings.maxGlycans,
		parameters.glycosylationSettings.allPeptides,
		parameters.modificationSettings.modifications,
		parameters.modificationSettings.maxModifications
	);

	let isReady = $derived(parameters.fasta !== undefined && !glamBusy);

	function onFinish() {
		glam.postMessage(JSON.stringify(parameters));
		glamBusy = true;
	}

	// Step Components
	const steps = [
		{
			title: 'Generate Peptides',
			component: GeneratePeptides
		},
		{
			title: 'Attach Glycans',
			component: AttachGlycans
		}
	];
</script>

<article
	class="w-max-[80%] card border-surface-200-800 preset-filled-surface-100-900 m-8 flex flex-col gap-4 border-2 p-4 text-center"
>
	<Stepper {steps} {isReady} {onFinish} />
	{#if glamBusy}
		<Progress value={null} />
	{/if}
</article>
