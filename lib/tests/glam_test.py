from pathlib import Path
from glam import DIGESTIONS, GLYCOSYLATION_MOTIFS, MODIFICATIONS, generate_glycopeptides

# Test Data  ===================================================================

SPIKE_PROTEIN: str = Path("tests/data/algal_spike.faa").read_text()
CHLAMY_GLYCANS: str = Path("tests/data/chlamy_glycans.csv").read_text()

# Integration Tests ============================================================


def test_basic(regtest) -> None:
    glycopeptides = generate_glycopeptides(
        SPIKE_PROTEIN,
        digestion=DIGESTIONS["Trypsin"],
        glycans=CHLAMY_GLYCANS,
        motif=GLYCOSYLATION_MOTIFS["N"],
    )
    regtest.write(glycopeptides[0][1])


def test_all_peptides(regtest) -> None:
    glycopeptides = generate_glycopeptides(
        SPIKE_PROTEIN,
        digestion=DIGESTIONS["Trypsin"],
        glycans=CHLAMY_GLYCANS,
        motif=GLYCOSYLATION_MOTIFS["N"],
        all_peptides=True,
    )
    regtest.write(glycopeptides[0][1])


def test_modifications(regtest) -> None:
    glycopeptides = generate_glycopeptides(
        SPIKE_PROTEIN,
        digestion=DIGESTIONS["Trypsin"],
        glycans=CHLAMY_GLYCANS,
        motif=GLYCOSYLATION_MOTIFS["N"],
        max_glycans=1,
        modifications=MODIFICATIONS.values(),
    )
    regtest.write(glycopeptides[0][1])


def test_modifications_all_peptides(regtest) -> None:
    glycopeptides = generate_glycopeptides(
        SPIKE_PROTEIN,
        digestion=DIGESTIONS["Trypsin"],
        glycans=CHLAMY_GLYCANS,
        motif=GLYCOSYLATION_MOTIFS["N"],
        max_glycans=1,
        all_peptides=True,
        modifications=MODIFICATIONS.values(),
    )
    regtest.write(glycopeptides[0][1])
