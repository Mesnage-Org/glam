import { getContext, setContext } from 'svelte';

const initDataKey = Symbol('initData');
const parametersKey = Symbol('parameters');

export function setInitData(initData: InitData) {
	setContext(initDataKey, initData);
}

export function getInitData(): InitData {
	return getContext(initDataKey);
}

export function setParameters(parameters: Parameters) {
	setContext(parametersKey, parameters);
}

export function getParameters(): Parameters {
	return getContext(parametersKey);
}

export class InitData {
	digestions: Map<string, string> | undefined = $state();
	glycosylationMotifs: Map<string, string> | undefined = $state();
	modifications: Map<string, [string, string[], number]> | undefined = $state();
}

export class Parameters {
	fasta: string | undefined = $state();
	digestSettings: DigestSettings = $state(new DigestSettings());
	glycans: string | undefined = $state();
	glycosylationSettings: GlycosylationSettings = $state(new GlycosylationSettings());
	modificationSettings: ModificationSettings = $state(new ModificationSettings());

	toJSON() {
		return {
			fasta: this.fasta,
			digestion: this.digestSettings.digestion,
			missedCleavages: this.digestSettings.missedCleavages,
			minLength: this.digestSettings.minLength,
			maxLength: this.digestSettings.maxLength,
			semiEnzymatic: this.digestSettings.semiEnzymatic,
			glycans: this.glycans,
			motif: this.glycosylationSettings.motif,
			maxGlycans: this.glycosylationSettings.maxGlycans,
			allPeptides: this.glycosylationSettings.allPeptides,
			modifications: this.modificationSettings.modifications,
			maxModifications: this.modificationSettings.maxModifications
		};
	}
}

class DigestSettings {
	digestion: string = $state('');
	missedCleavages: number = $state(0);
	minLength: number | null = $state(null);
	maxLength: number | null = $state(null);
	semiEnzymatic: boolean = $state(false);
}

class GlycosylationSettings {
	motif: string = $state('');
	maxGlycans: number | null = $state(null);
	allPeptides: boolean = $state(false);
}

class ModificationSettings {
	modifications: [string, string[], number][] = $state([]);
	maxModifications: number | null = $state(null);
}
