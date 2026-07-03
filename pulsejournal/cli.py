#!/usr/bin/env python3
"""
PulseJournal — Your body has a story to tell.
================================================
Turn Apple Health export data into a natural-language diary entry.
Powered by Ollama — your data never leaves your Mac.

Usage:
  python -m pulsejournal.cli generate --input health_export.zip --tone hero
"""

import sys
from pathlib import Path

import click
from rich.console import Console

from pulsejournal.ollama_client import check_ollama, generate_entry
from pulsejournal.parser import parse_export
from pulsejournal.tones import TONE_CHOICES, TONES

console = Console()


# ── CLI ───────────────────────────────────────────────────────────────────────

@click.group()
def cli():
    """📔  PulseJournal — turn Apple Health data into a diary entry.\n
    \b
    Quick start:
      python -m pulsejournal.cli generate --input health_export.zip --tone hero
    """
    pass


@cli.command()
@click.option(
    "--input", "input_path",
    required=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="Path to the Apple Health export ZIP.",
)
@click.option(
    "--tone",
    type=click.Choice(TONE_CHOICES),
    default="reflective",
    show_default=True,
    help="Narrative voice for the generated entry.",
)
def generate(input_path: Path, tone: str):
    """Generate a diary entry from an Apple Health export."""

    console.print(f"\n[bold amber3]📔 PulseJournal[/bold amber3] — generating [cyan]{TONES[tone]['label']}[/cyan] entry\n")

    console.print("[dim]Checking Ollama connection...[/dim]")
    if not check_ollama():
        console.print(
            "[bold red]✗ Cannot reach Ollama.[/bold red]\n"
            "  Make sure Ollama is running: [bold]ollama serve[/bold]"
        )
        sys.exit(1)
    console.print("[green]✓ Ollama connected[/green]\n")

    try:
        metrics = parse_export(input_path)
        entry = generate_entry(metrics, tone)
    except NotImplementedError:
        console.print(
            "[yellow]Parsing and generation aren't implemented yet — "
            "this is scaffolding for a follow-up step.[/yellow]"
        )
        return

    console.print(entry)


if __name__ == "__main__":
    cli()
