<script lang="ts">
	let { steps, isReady, onFinish } = $props();

	// Icons
	import { ArrowLeft, ArrowRight, Download } from 'lucide-svelte';

	// Reactive
	let currentStep = $state(0);
	const isFirstStep = $derived(currentStep === 0);
	const isLastStep = $derived(currentStep === steps.length - 1);

	function isCurrentStep(index: number): boolean {
		return currentStep === index;
	}

	function setStep(index: number) {
		currentStep = index;
	}

	function prevStep() {
		currentStep--;
	}

	function nextStep() {
		currentStep++;
	}
</script>

<div class="w-full">
	<!-- Stepper -->
	<div class="space-y-8">
		<!-- Timeline -->
		<div class="relative">
			<!-- Numerals -->
			<div class="flex items-center justify-between gap-4">
				{#each steps as step, i (step.title)}
					<!-- Numeral Button -->
					<button
						class="btn-icon btn-icon-sm rounded-full {isCurrentStep(i)
							? 'preset-filled-primary-500'
							: 'preset-filled-surface-200-800'}"
						onclick={() => setStep(i)}
						title={step.title}
					>
						<span class="font-bold">{i + 1}</span>
					</button>
				{/each}
			</div>
			<!-- Line -->
			<hr class="hr !border-surface-200-800 absolute top-[50%] right-0 left-0 z-[-1]" />
		</div>
		<!-- Loop all steps -->
		{#each steps as step, i (step)}
			<div class={['flex flex-col gap-4', !isCurrentStep(i) && 'hidden']}>
				<h4 class="h4">{step.title}</h4>
				<step.component {...step.props} />
			</div>
		{/each}
		<!-- Navigation -->
		<nav class="flex items-center justify-between gap-4">
			<!-- Back Button -->
			<button
				type="button"
				class="btn preset-tonal hover:preset-filled {isFirstStep ? 'invisible' : ''}"
				onclick={prevStep}
				disabled={isFirstStep}
			>
				<ArrowLeft size={18} />
				<span>Previous</span>
			</button>
			<!-- Next / Finish Button -->
			{#if !isLastStep}
				<button type="button" class="btn preset-tonal hover:preset-filled" onclick={nextStep}>
					<span>Next</span>
					<ArrowRight size={18} />
				</button>
			{:else}
				<button
					type="button"
					class={['btn preset-tonal-success', isReady && 'hover:preset-filled-success-700-300']}
					onclick={onFinish}
					disabled={!isReady}
				>
					<span>Run Analysis</span>
					<Download size={18} />
				</button>
			{/if}
		</nav>
	</div>
</div>
