<script lang="ts">
	let { steps } = $props();

	// Icons
	import { ArrowLeft, ArrowRight } from 'lucide-svelte';

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

<div class="w-full max-w-min">
	<!-- Stepper -->
	<div class="space-y-4">
		<!-- Timeline -->
		<div class="relative">
			<!-- Numerals -->
			<div class="flex items-center justify-between gap-4">
				{#each steps as step, i (step.title)}
					<!-- Numeral Button -->
					<button
						class="z-10 rounded-xl px-2 py-1 text-sm {isCurrentStep(i)
							? 'preset-filled-primary-500'
							: 'preset-filled-surface-200-800'}"
						onclick={() => setStep(i)}
						title={step.title}
					>
						<span class="font-bold">{i + 1}. {step.title}</span>
					</button>
				{/each}
			</div>
			<!-- Line -->
			<hr class="hr !border-surface-200-800 absolute top-[50%] right-0 left-0 border-t-2" />
		</div>
		<!-- Loop all steps -->
		{#each steps as step, i (step)}
			<div class={['flex flex-col gap-4', !isCurrentStep(i) && 'hidden']}>
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
			{/if}
		</nav>
	</div>
</div>
