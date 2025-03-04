<script lang="ts">
	import { getParameters } from '$lib/state.svelte';

	import { CircleX, CirclePlus } from 'lucide-svelte';

	let joinedModifications: [string, string, number][] = $state([]);

	let modificationSettings = getParameters().modificationSettings;

	// NOTE: Using `$effect` to overwrite `joinedModifications` if the user changed `modifications` via the `Built-In` tab
	$effect(() => {
		joinedModifications = modificationSettings.modifications.map(([abbr, targets, offset]) => [
			abbr,
			targets.filter((t) => t !== '').join(', '),
			offset
		]);
	});

	function onchange() {
		const mods = joinedModifications.map(([abbr, targets, offset]): [string, string[], number] => [
			abbr,
			targets.split(',').map((s) => s.trim()),
			offset
		]);

		modificationSettings.modifications = mods;
	}
</script>

<form class="grid w-full grid-cols-[1fr_1fr_1fr_auto] gap-2">
	{#if joinedModifications.length !== 0}
		<label class="label label-text" for="abbr">Abbreviation</label>
		<label class="label label-text" for="targets">Target Residues</label>
		<label class="label label-text" for="offset">Mass Offset</label>
	{/if}
	{#each joinedModifications as value, i}
		<input class="input col-start-1" type="text" name="abbr" bind:value={value[0]} {onchange} />
		<input class="input" type="text" name="targets" bind:value={value[1]} {onchange} />
		<input class="input" type="number" name="offset" bind:value={value[2]} {onchange} />
		<button
			type="button"
			class="btn-icon hover:preset-tonal"
			onclick={() => {
				joinedModifications.splice(i, 1);
				onchange();
			}}><CircleX /></button
		>
	{/each}
	<button
		type="button"
		class="btn-icon preset-tonal hover:preset-filled col-span-full w-full"
		onclick={() => {
			joinedModifications.push(['', '', 0]);
			onchange();
		}}><CirclePlus /></button
	>
</form>
