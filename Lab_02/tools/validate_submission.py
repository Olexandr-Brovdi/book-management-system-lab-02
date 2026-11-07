"""Check submission identity and variant requirements without external packages.

This does not emulate or promise the external checker's status.
"""

import re
from pathlib import Path
from xml.etree import ElementTree
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def report_text(path: Path) -> str:
    with ZipFile(path) as archive:
        xml = ElementTree.fromstring(archive.read("word/document.xml"))
    return "\n".join("".join(t.itertext()) for t in xml.iter(W + "t"))


def validate() -> None:
    reports = [
        ROOT / "docs/Lab_02_Report_Variant_2.docx",
        ROOT / "Lab_02/report/report.docx",
    ]
    # The standalone Lab_02 folder may have only its canonical report.
    if ROOT.name == "Lab_02":
        reports = [ROOT / "report/report.docx"]
    for path in reports:
        text = report_text(path)
        flattened = re.sub(r"\s+", " ", text).casefold()
        for phrase in (
            "лабораторної роботи №2",
            "варіант №2",
            "бровді олександр",
            "аналіз системи обліку книг",
            "унікальн",
            "групуван",
            "пошук",
            "фільтрац",
            "найбільш",
            "середн",
            "сортуван",
            "counter",
            "closure",
            "decorator",
            "benchmark",
        ):
            if phrase not in flattened:
                raise ValueError(f"{path.name}: missing {phrase}")
        variants = re.findall(r"варіант\s*№?\s*(\d+)", flattened)
        if not variants or set(variants) != {"2"}:
            raise ValueError(f"Conflicting variants: {variants}")
        if any(
            term in flattened
            for term in (
                "заставний денис",
                "student_grading",
                "система оцінювання студентів",
            )
        ):
            raise ValueError("Unrelated sample content in report")
    if len(reports) == 2 and reports[0].read_bytes() != reports[1].read_bytes():
        raise ValueError("Report copies differ")
    actual = {p.resolve() for p in ROOT.rglob("*.docx") if ".venv" not in p.parts}
    if actual != {p.resolve() for p in reports}:
        raise ValueError("Unexpected or missing report files")
    print("PASS: Lab_02, variant 2, author, book topic and requirements match.")


if __name__ == "__main__":
    validate()
