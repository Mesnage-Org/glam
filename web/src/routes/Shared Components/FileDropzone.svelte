<script lang="ts">
	let { onFileAccept, subtext, accept } = $props();

	// External Componenents
	import { FileUpload } from '@skeletonlabs/skeleton-svelte';

	// Icons
	import { ImagePlus, Paperclip, CircleX } from 'lucide-svelte';
</script>

<FileUpload
	onFileAccept={async (f: any) => onFileAccept(await f.files[0].text())}
	classes="w-full grow flex! flex-col"
	interfaceClasses="grow justify-center-safe"
	{subtext}
	{accept}
>
	{#snippet iconInterface()}<ImagePlus class="size-8" />{/snippet}
	{#snippet iconFile()}<Paperclip class="size-4" />{/snippet}
	{#snippet iconFileRemove()}<CircleX class="size-4" />{/snippet}
</FileUpload>
