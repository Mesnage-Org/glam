# Imports ==============================================================================

# Standard Library
from io import StringIO
from typing import Iterable, Pattern, NamedTuple
import csv
import itertools
from re import Match
import re

# Dependencies
from pyteomics.auxiliary import PyteomicsError
import glycowork.motif.tokenization as glycowork
import pyteomics.mass
import pyteomics.parser

# Constants ============================================================================

# NOTE: Not quite the monoisotopic water mass that the most accurate mass calculators
# produce, but it is what `glycowork` seems to be using
WATER_MASS: float = 18.0105546

# Types ================================================================================

type Regex = str | Pattern[str]


class Modification(NamedTuple):
    abbreviation: str
    targeted_residues: list[str]
    mass_delta: float


# NOTE: Inheriting from `NamedTuple` gives us the immutability we need to store these
# values in a `set`, and it also makes the fields easy to unpack!
class Glycan(NamedTuple):
    name: str
    mass: float


class Peptide(NamedTuple):
    sequence: str
    mass: float | None = None
    sites: tuple[str, ...] | None = None


class Glycopeptide(NamedTuple):
    sequence: str
    mass: float
    sites: tuple[str, ...]


# Functions ============================================================================


def glycan_mass(glycan_name: str) -> float:
    mass = 0.0

    # Try to parse the string as a fully-defined structure first
    try:
        mass = glycowork.glycan_to_mass(glycan_name)
    except KeyError:
        # But if that fails, then try just parsing it as a sugar composition
        try:
            mass = glycowork.composition_to_mass(glycan_name)
        except IndexError:
            pass

    # NOTE: Many nonsense structures / compositions just return the mass of water — if
    # the result was just a water mass, then whatever we were given wasn't valid, so
    # throw an error as if `mass` were never set
    if mass in [0, WATER_MASS]:
        raise ValueError(f"Invalid glycan structure / composition: '{glycan_name}'")
    else:
        return mass


def load_glycans(glycan_csv: str) -> set[Glycan]:
    expected_cols = ["Glycan", "Monoisotopic Mass"]

    try:
        rows = csv.reader(StringIO(glycan_csv))
    except Exception as e:
        raise ValueError(f"Failed to read glycan CSV: {e}")

    header = next(rows)

    if header == expected_cols:
        return {Glycan(g, float(m)) for g, m in rows}
    elif header == expected_cols[:1]:
        return {Glycan(g, glycan_mass(g)) for (g,) in rows}
    else:
        raise ValueError(
            "The glycan file must contain either the columns "
            f"{expected_cols} or just {expected_cols[:1]}"
        )


# TODO: Also report peptide positions / indicies?
def digest_protein(
    seq: str,
    rule: Regex,
    missed_cleavages: int,
    min_length: int | None,
    max_length: int | None,
    semi_enzymatic: bool,
) -> set[Peptide]:
    return {
        Peptide(p)
        for p in pyteomics.parser.cleave(
            seq,
            rule,
            missed_cleavages,
            min_length,
            max_length,
            semi_enzymatic,
            None,
            True,
        )
    }


def modify_peptides(
    peptides: set[Peptide],
    mods: Iterable[Modification],
    max_mods: int | None = None,
) -> set[Peptide]:
    variable_mods = {n: ts for (n, ts, _) in mods}
    return {
        peptide._replace(sequence=isoform)
        for peptide in peptides
        for isoform in pyteomics.parser.isoforms(
            peptide.sequence, variable_mods=variable_mods
        )
    }


def find_glycosylation_sites(
    peptides: set[Peptide], glycosylation_motif: Regex
) -> set[Peptide]:
    def find_sites(peptide: Peptide) -> tuple[str, ...]:
        def name_site(match: Match[str]):
            residue = match.group()
            index = match.start() + 1

            index -= sum(c.islower() for c in peptide.sequence[:index])

            return f"{residue}{index}"

        # NOTE: This is a `tuple` and not a `list` or `set` because only `tuple`s are hashable! It needs to be a
        # hashable type so that it can be collected into a `set`!
        return tuple(
            name_site(m) for m in re.finditer(glycosylation_motif, peptide.sequence)
        )

    return {p._replace(sites=find_sites(p)) for p in peptides}


def filter_glycopeptide_candidates(
    peptides: set[Peptide],
) -> set[Peptide]:
    return {p for p in peptides if p.sites is not None and len(p.sites) != 0}


def peptide_masses(
    peptides: set[Peptide], mods: Iterable[Modification] = []
) -> set[Peptide]:
    def mass(peptide: Peptide) -> float:
        mod_masses = {n: m for (n, _, m) in mods}
        aa_mass = pyteomics.mass.std_aa_mass | mod_masses
        try:
            return pyteomics.mass.fast_mass2(peptide.sequence, aa_mass=aa_mass)
        except PyteomicsError as e:
            raise ValueError(
                f"Unknown amino acid residue found in '{peptide.sequence}': {e.message}"
            )

    return {peptide._replace(mass=mass(peptide)) for peptide in peptides}


def build_glycopeptides(
    peptides: set[Peptide], glycans: set[Glycan], all_peptides: bool
) -> set[Glycopeptide]:
    def to_glycopeptide(peptide: Peptide) -> Glycopeptide:
        sequence, mass, sites = peptide

        # Ensure the `Peptide` is fully initialized
        assert mass is not None
        assert sites is not None

        return Glycopeptide(sequence, mass, sites)

    def build(peptide: Peptide, glycan: Glycan) -> Glycopeptide:
        glycopeptide = to_glycopeptide(peptide)

        name = f"{glycan.name}-{glycopeptide.sequence}"
        # This is a condensation reaction, so remember to take away a water mass
        mass = glycan.mass + glycopeptide.mass - WATER_MASS

        return glycopeptide._replace(sequence=name, mass=mass)

    glycopeptide_candidates = filter_glycopeptide_candidates(peptides)
    glycopeptides = {
        build(p, g) for p, g in itertools.product(glycopeptide_candidates, glycans)
    }

    # TODO: If `glycopeptides` or `glycans` is empty, I should automatically include the
    # non-glycopeptides!
    if all_peptides:
        glycopeptides |= {to_glycopeptide(p) for p in peptides}

    return glycopeptides


def convert_to_csv(glycopeptides: set[Glycopeptide]) -> str:
    csv_str = StringIO()
    writer = csv.writer(csv_str)
    writer.writerow(["Structure", "Monoisotopic Mass"])

    # FIXME: Use a sort key instead of this odd approach...
    # FIXME: Actually do something with the `sites` value!
    sorted_glycopeptides = sorted(
        (("-" in name, mass, name) for name, mass, *_ in glycopeptides), reverse=True
    )

    for _, mass, name in sorted_glycopeptides:
        mass = round(mass, 6)
        # NOTE: This is a nasty hack for PGFinder, which expects a `|1` type suffix
        # after the name of each structure. Really, that's a design flaw in PGFinder,
        # but we'll fix it here for now...
        hacky_name = f"{name}|1"
        writer.writerow([hacky_name, mass])

    return csv_str.getvalue()
