# Imports ==============================================================================

# Standard Library
from pathlib import Path

# Dependencies
from pyteomics import fasta
import pytest

# Local Modules
from glam import DIGESTIONS, GLYCOSYLATION_MOTIFS, MODIFICATIONS
from glam._lib import (
    WATER_MASS,
    glycan_mass,
    load_glycans,
    digest_protein,
    modify_peptides,
    filter_glycopeptides,
    peptide_masses,
    build_glycopeptides,
    convert_to_csv,
)

# Test Data  ===========================================================================

# Inputs
SPIKE_PROTEIN: str = next(fasta.read("tests/data/algal_spike.faa")).sequence
GLYCANS: str = Path("tests/data/chlamy_glycans.csv").read_text()
GLYCANS_AND_MASSES: str = Path("tests/data/chlamy_glycans_and_masses.csv").read_text()

# Expected Outputs
TRYPTIC_PEPTIDES: set[str] = set(
    Path("tests/data/tryptic_peptides.txt").read_text().splitlines()
)
GLYCOPEPTIDES: set[str] = set(
    Path("tests/data/glycopeptides.txt").read_text().splitlines()
)
CSV: str = Path("tests/data/csv.csv").read_text().replace("\n", "\r\n")


# Unit Tests ===========================================================================


def test_glycan_mass() -> None:
    iupac_structure = "Neu5Ac(a2-3)Gal6S(b1-3)[Neu5Ac(a2-6)]GalNAc"
    assert glycan_mass(iupac_structure) == 1045.2903546

    byonic_composition = "HexNAc(2)Hex(3)Pent(1)dHex(1)"
    assert glycan_mass(byonic_composition) == 1188.4279546

    oxford_notation = "FA2G2S1"
    assert glycan_mass(oxford_notation) == 2077.7454546


def test_glycan_mass_raises() -> None:
    nonsense_structure = "gm-AEJA"
    with pytest.raises(ValueError) as e:
        glycan_mass(nonsense_structure)
    assert str(e.value) == "Invalid glycan structure / composition: 'gm-AEJA'"

    just_numbers = "123"
    with pytest.raises(ValueError) as e:
        print(glycan_mass(just_numbers))
    assert str(e.value) == "Invalid glycan structure / composition: '123'"

    empty = ""
    with pytest.raises(ValueError) as e:
        print(glycan_mass(empty))
    assert str(e.value) == "Invalid glycan structure / composition: ''"


def test_load_glycans_with_masses() -> None:
    glycans = load_glycans(GLYCANS_AND_MASSES)
    assert len(glycans) == 52
    assert all(type(g) is str and type(m) is float for g, m in glycans)


def test_load_glycans_without_masses() -> None:
    glycans = load_glycans(GLYCANS)
    assert len(glycans) == 52
    assert all(type(g) is str and type(m) is float for g, m in glycans)

    expected_glycans = load_glycans(GLYCANS_AND_MASSES)
    assert glycans == expected_glycans


def test_load_glycans_raises() -> None:
    no_header = GLYCANS_AND_MASSES.removeprefix("Glycan,Monoisotopic Mass\n")
    with pytest.raises(ValueError) as e:
        load_glycans(no_header)
    assert str(e.value) == (
        "The glycan file must contain either the columns "
        "['Glycan', 'Monoisotopic Mass'] or just ['Glycan']"
    )


def test_digest_protein() -> None:
    tryptic_peptides = digest_protein(
        SPIKE_PROTEIN, DIGESTIONS["Trypsin"], 0, None, None, False
    )
    assert len(tryptic_peptides) == 90
    assert tryptic_peptides == TRYPTIC_PEPTIDES


def test_modify_peptides() -> None:
    peptides = {"CARNAGE", "CATS"}
    modified_peptides = {
        "CARNAGE",
        "cmCARNAGE",
        "CARdaNAGE",
        "cmCARdaNAGE",
        "CATS",
        "cmCATS",
    }
    assert modify_peptides(peptides, MODIFICATIONS.values()) == modified_peptides


def test_filter_glycopeptides() -> None:
    tryptic_peptides = digest_protein(
        SPIKE_PROTEIN, DIGESTIONS["Trypsin"], 0, None, None, False
    )
    glycopeptides = filter_glycopeptides(tryptic_peptides, GLYCOSYLATION_MOTIFS["N"])
    assert len(glycopeptides) == 15
    assert glycopeptides == GLYCOPEPTIDES


def test_peptide_masses() -> None:
    masses = peptide_masses({"PEPTIDE", "TIME"})
    assert masses == {("PEPTIDE", 799.3599640267099), ("TIME", 492.2253851302)}


def test_modified_peptide_masses() -> None:
    masses = peptide_masses({"PcmEPTIdaDE"}, mods=MODIFICATIONS.values())
    assert masses == {("PcmEPTIdaDE", 799.3599640267099 + 57.021464 + 0.984016)}


def test_peptide_masses_raises() -> None:
    with pytest.raises(ValueError) as e:
        peptide_masses({"PEPTIXE"})
    assert str(e.value) == (
        "Unknown amino acid residue found in 'PEPTIXE': "
        "Mass not specified for label(s): X"
    )


def test_build_glycopeptides() -> None:
    peptides = {("PEP", WATER_MASS + 0.2), ("TIDE", WATER_MASS + 0.1)}
    glycans = {("A", 1.0), ("AB", 20.0), ("ABC", 300.0)}
    glycopeptides = {
        ("A-PEP", 1.2),
        ("AB-PEP", 20.2),
        ("ABC-PEP", 300.2),
        ("A-TIDE", 1.1),
        ("AB-TIDE", 20.1),
        ("ABC-TIDE", 300.1),
    }
    # NOTE: Probably shouldn't be using `float`s for any of these calculations... The
    # floating-point error means that we end up with things like `1.1000000000000014`
    # instead of `1.1`... Look into replacing all of the `float`s with `Decimal`? For
    # now, we'll just round the masses returned from `build_glycopeptides`...
    rounded_glycopeptides = {
        (n, round(m, ndigits=1)) for n, m in build_glycopeptides(peptides, glycans)
    }
    assert rounded_glycopeptides == glycopeptides


def test_convert_to_csv() -> None:
    glycopeptides = {
        ("A", 42.123456789),
        ("B", 128.123456789),
        ("C", 1337.123456789),
    }
    csv = convert_to_csv(glycopeptides)
    assert csv == CSV
