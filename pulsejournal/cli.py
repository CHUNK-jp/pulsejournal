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

from pulsejournal.ollama_client import GENERATION_MODEL, check_ollama, generate_entry, has_generation_model
from pulsejournal.parser import parse_export
from pulsejournal.tones import LANG_CHOICES, TONE_CHOICES, TONES

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
@click.option(
    "--lang",
    type=click.Choice(LANG_CHOICES),
    default="en",
    show_default=True,
    help="Language of the generated entry.",
)
def generate(input_path: Path, tone: str, lang: str):
    """Generate a diary entry for the most recent day in an Apple Health export."""

    console.print(f"\n[bold amber3]📔 PulseJournal[/bold amber3] — generating [cyan]{TONES[tone]['label']}[/cyan] entry\n")

    console.print("[dim]Checking Ollama connection...[/dim]")
    if not check_ollama():
        console.print(
            "[bold red]✗ Cannot reach Ollama.[/bold red]\n"
            "  Make sure Ollama is running: [bold]ollama serve[/bold]"
        )
        sys.exit(1)
    if not has_generation_model():
        console.print(
            f"[bold red]✗ Model '{GENERATION_MODEL}' isn't pulled yet.[/bold red]\n"
            f"  Run: [bold]ollama pull {GENERATION_MODEL}[/bold]"
        )
        sys.exit(1)
    console.print(f"[green]✓ Ollama connected[/green] (model: {GENERATION_MODEL})\n")

    daily_metrics = parse_export(input_path)
    if not daily_metrics:
        console.print("[yellow]No health records found in that export.[/yellow]")
        return

    latest_day = daily_metrics[-1]
    entry = generate_entry(latest_day, tone, lang)

    console.print(entry)


if __name__ == "__main__":
    cli()
