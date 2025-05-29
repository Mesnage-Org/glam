import { base } from '$app/paths';
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
	indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.27.6/full/'
});

const minimalDependencies = [
	// Needed by glycowork
	'pandas',
	'networkx',
	'scipy',
	'scikit-learn', // ?
	'ipython', // ?
	'https://files.pythonhosted.org/packages/32/30/532fe57467a6cc7ff2e39f088db1cb6d6bf522f724a4a5c7beda1282d5a6/huggingface_hub-0.32.2-py3-none-any.whl', // ?
	'https://files.pythonhosted.org/packages/7f/ca/a8e5ae0e13d7c874e138c5d0e8313856b91f97359781fd78b0c9e34ae791/drawsvg-2.4.0-py3-none-any.whl', // ?
	'https://files.pythonhosted.org/packages/c0/da/977ded879c29cbd04de313843e76868e6e13408a94ed6b987245dc7c8506/openpyxl-3.1.5-py2.py3-none-any.whl', // ?
	'https://files.pythonhosted.org/packages/15/62/07049f6b11cfffcb5b25454801f3ffc6c765888e351aebd31d5f8054489e/glycorender-0.2.0-py3-none-any.whl', // ?

	// Needed by huggingface_hub
	'requests',
	'tqdm',
	'pyyaml',
	'https://files.pythonhosted.org/packages/4d/36/2a115987e2d8c300a974597416d9de88f2444426de9571f4b59b2cca3acc/filelock-3.18.0-py3-none-any.whl',

	// Needed by openpyxl
	'https://files.pythonhosted.org/packages/c1/8b/5fe2cc11fee489817272089c4203e679c63b570a5aaeb18d852ae3cbba6a/et_xmlfile-2.0.0-py3-none-any.whl',

	// Needed by glycorender
	'https://files.pythonhosted.org/packages/a1/2e/7994a139150abf11c8dd258feb091ad654823a83cfd9720bfdded27185c3/reportlab-4.4.1-py3-none-any.whl',

	'https://files.pythonhosted.org/packages/fb/62/b5d706255739553398d3a308d92e2476d5a363ad3ca0598c51bc75cc5054/pyteomics-4.7.5-py3-none-any.whl',
	'https://files.pythonhosted.org/packages/cb/37/c7ad190ceb30a760de631994bd076b418cd621f93835ac0a6ed95384ce7e/glycowork-1.6.1-py3-none-any.whl',
	`${base}/theglam-1.2.0-py3-none-any.whl`,
]

await pyodide.loadPackage(minimalDependencies);
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
		fasta,
		digestion,
		missedCleavages,
		minLength,
		maxLength,
		semiEnzymatic,
		glycans,
		motif,
		maxGlycans,
		allPeptides,
		modifications,
		maxModifications
	} = JSON.parse(parameters);
	const csvFiles = convert(
		generate_glycopeptides(
			fasta,
			digestion,
			missedCleavages,
			minLength,
			maxLength,
			semiEnzymatic,
			glycans,
			motif,
			maxGlycans,
			allPeptides,
			modifications,
			maxModifications
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
