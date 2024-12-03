from pathlib import Path
from glam import DIGESTIONS, GLYCOSYLATION_MOTIFS, generate_glycopeptides

# Test Data  ===================================================================

SPIKE_PROTEIN: str = Path("tests/data/algal_spike.faa").read_text()
CHLAMY_GLYCANS: str = Path("tests/data/chlamy_glycans.csv").read_text()

# Integration Tests ============================================================


def test_basic(regtest) -> None:
    glycopeptides = generate_glycopeptides(
        SPIKE_PROTEIN, DIGESTIONS["Trypsin"], GLYCOSYLATION_MOTIFS["N"], CHLAMY_GLYCANS
    )
    regtest.write(glycopeptides[0][1])


def test_all_peptides(regtest) -> None:
    glycopeptides = generate_glycopeptides(
        SPIKE_PROTEIN,
        DIGESTIONS["Trypsin"],
        GLYCOSYLATION_MOTIFS["N"],
        CHLAMY_GLYCANS,
        all_peptides=True,
    )
    regtest.write(glycopeptides[0][1])
