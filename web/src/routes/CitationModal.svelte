<script lang="ts">
	import { Modal } from '@skeletonlabs/skeleton-svelte';

	let openState = $state(false);
</script>

<Modal
	open={openState}
	onOpenChange={(e: any) => (openState = e.open)}
	triggerBase="text-2xl hover:underline"
	contentBase="card bg-surface-100-900 p-4 space-y-4 shadow-xl w-3xl max-h-9/10 overflow-auto"
	backdropClasses="backdrop-blur-sm"
>
	{#snippet trigger()}Cite Us!{/snippet}
	{#snippet content()}
		<header class="flex justify-between">
			<h2 class="h2">Cite Us!</h2>
		</header>
		<article>
			<div class="space-y-4">
				<p class="text-sm">
					Alamán-Zárate, M. G. <i>et al.</i> A software tool and strategy for peptidoglycomics, the
					high-resolution analysis of bacterial peptidoglycans via LC-MS/MS. <i>Commun Chem</i>
					<b>8</b>, 1–12 (2025). <br />
					<a href="https://doi.org/10.1038/s42004-025-01490-6" class="anchor" target="_blank"
						>https://doi.org/10.1038/s42004-025-01490-6</a
					>
				</p>
				<p class="text-sm">
					Patel, A. V. <i>et al.</i> PGFinder, a novel analysis pipeline for the consistent,
					reproducible, and high-resolution structural analysis of bacterial peptidoglycans.
					<i>eLife</i> <b>10</b>, e70597 (2021). <br />
					<a href="https://doi.org/10.7554/eLife.70597" class="anchor" target="_blank"
						>https://doi.org/10.7554/eLife.70597</a
					>
				</p>
				<p class="text-sm">
					Rady, B. J. &amp; Mesnage, S. PGFinder, an Open-Source Software for Peptidoglycomics: The
					Structural Analysis of Bacterial Peptidoglycan by LC-MS. <i>Methods Mol Biol</i>
					<b>2836</b>, 111–132 (2024). <br />
					<a href="https://doi.org/10.1007/978-1-0716-4007-4_8" class="anchor" target="_blank"
						>https://doi.org/10.1007/978-1-0716-4007-4_8</a
					>
				</p>
			</div>
		</article>
	{/snippet}
</Modal>
