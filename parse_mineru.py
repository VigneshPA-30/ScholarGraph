from pathlib import Path
import subprocess
import argparse
import os


# Path to the MinerU executable in the separate venv
MINERU_EXE = Path("mineru_venv") / "Scripts" / "mineru.exe"


def parse_pdf(pdf_path: str, output_dir: str):

    env = os.environ.copy()
    env["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
    env["HF_HOME"] = str(Path("models_cache").resolve())
    pdf = Path(pdf_path).resolve()

    if not pdf.exists():
        raise FileNotFoundError(f"{pdf} not found.")

    output = Path(output_dir).resolve()
    output.mkdir(parents=True, exist_ok=True)

    if not MINERU_EXE.exists():
        raise FileNotFoundError(
            f"MinerU executable not found:\n{MINERU_EXE.resolve()}\n"
            "Did you create/install MinerU in mineru_venv?"
        )

    command = [
        str(MINERU_EXE.resolve()),
        "-p",
        str(pdf),
        "-o",
        str(output),
        "-b",
        "pipeline",  # CPU backend
    ]

    print("Running MinerU...\n")
    print(" ".join(command))
    print()

    result = subprocess.run(command)

    if result.returncode != 0:
        raise RuntimeError(f"MinerU failed with exit code {result.returncode}")

    print("\nDone!\n")
    print("Generated files:\n")

    for file in sorted(output.rglob("*")):
        print(file.relative_to(output))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--pdf",
        required=True,
        help="Path to the PDF file"
    )

    parser.add_argument(
        "--output",
        default="parsed_output",
        help="Output directory"
    )

    args = parser.parse_args()

    parse_pdf(args.pdf, args.output)