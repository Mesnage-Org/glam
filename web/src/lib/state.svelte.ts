import { getContext, setContext } from 'svelte';

let initDataKey = Symbol('initData');
let parametersKey = Symbol('parameters');

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
	proteinFasta: string | undefined = $state();
	digestSettings: DigestSettings = $state(new DigestSettings());
	glycanCsv: string | undefined = $state();
	glycosylationSettings: GlycosylationSettings = $state(new GlycosylationSettings());
	modificationSettings: ModificationSettings = $state(new ModificationSettings());

	toJSON() {
		return {
			proteinFasta: this.proteinFasta,
			digestions: this.digestSettings.regex,
			missedCleavages: this.digestSettings.missedCleavages,
			minLength: this.digestSettings.minLength,
			maxLength: this.digestSettings.maxLength,
			semiEnzymatic: this.digestSettings.semiEnzymatic,
			glycanCsv: this.glycanCsv,
			motifs: this.glycosylationSettings.regex,
			allPeptides: this.glycosylationSettings.allPeptides,
			modifications: this.modificationSettings.modifications,
			maxModifications: this.modificationSettings.maxModifications
		};
	}
}

class DigestSettings {
	regex: string = $state('');
	missedCleavages: number = $state(0);
	minLength: number | null = $state(null);
	maxLength: number | null = $state(null);
	semiEnzymatic: boolean = $state(false);
}

class GlycosylationSettings {
	regex: string = $state('');
	allPeptides: boolean = $state(false);
}

class ModificationSettings {
	modifications: [string, string[], number][] = $state([]);
	maxModifications: number | null = $state(null);
}
