import { loadPyodide } from 'pyodide';

// FIXME: Any type...
function convert(proxy: any) {
	let val = proxy.toJs({ dict_converter: Object.fromEntries });
	proxy.destroy();
	return val;
}

function global(name: string) {
	let proxy = pyodide.globals.get(name);
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
// NOTE: `glycowork` pulls in an insane number of deps... This is one of them
await micropip.install('requests');
await micropip.install('theglam==1.1.0');
// If you need to test development version of pgfinder you should build the wheel and copy the resulting .whl to the
// lib/ directory (adajacent to this file), replace the version below and comment out the above (which loads from
// PyPI).
// await micropip.install('./theglam-1.0.0-py3-none-any.whl');
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
