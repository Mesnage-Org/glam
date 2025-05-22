import { loadPyodide } from 'pyodide';

// FIXME: Any type...
function convert(proxy: any) {
	const val = proxy.toJs({ dict_converter: Object.fromEntries });
	proxy.destroy();
	return val;
}

function global(name: string) {
	const proxy = pyodide.globals.get(name);
	return convert(proxy);
}

// NOTE: This version needs to match the version of pyodide installed by npm!
// These files can also be hosted locally from `/static` if something ever
// happens to this CDN, but there will be some build-system demons to battle.
const pyodide = await loadPyodide({
	indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.27.5/full/'
});

await pyodide.loadPackage(['micropip']);
const micropip = pyodide.pyimport('micropip');

await micropip.install(`${self.location.origin}/theglam-1.2.0-py3-none-any.whl`);
await pyodide.runPythonAsync('from glam import *');
const generate_glycopeptides = pyodide.globals.get('generate_glycopeptides');

const msg = {
	type: 'Ready',
	initData: {
		digestions: global('DIGESTIONS'),
		glycosylationMotifs: global('GLYCOSYLATION_MOTIFS'),
		modifications: global('MODIFICATIONS')
	}
};
postMessage(msg);

onmessage = ({ data: parameters }) => {
	const {
		proteinFasta,
		digestions,
		missedCleavages,
		minLength,
		maxLength,
		semiEnzymatic,
		glycanCsv,
		motifs,
		allPeptides,
		modifications,
		maxModifications
	} = JSON.parse(parameters);
	const csvFiles = convert(
		generate_glycopeptides(
			proteinFasta,
			digestions,
			motifs,
			glycanCsv,
			modifications,
			maxModifications,
			missedCleavages,
			minLength,
			maxLength,
			semiEnzymatic,
			allPeptides
		)
	);
	csvFiles.forEach(([filename, csv]: [any, any]) => {
		const blob = new Blob([csv], { type: 'text/csv' });
		const msg = {
			type: 'Result',
			filename,
			blob
		};
		postMessage(msg);
	});
};
