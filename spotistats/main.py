import argparse
import json
import os
import sys
from pathlib import Path
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from rich.console import Console
from . import ui

# --- CONFIGURATION PATHS ---
CONFIG_DIR = Path.home() / ".config" / "spotistats"
CONFIG_FILE = CONFIG_DIR / "config.json"
CACHE_FILE = CONFIG_DIR / ".cache"

console = Console()

def ensure_config_dir():
    """Ensures the configuration directory exists."""
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)

def load_config():
    """Loads configuration from JSON file."""
    if not CONFIG_FILE.exists():
        return None
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return None

def save_config(client_id, client_secret, redirect_uri):
    """Saves configuration to JSON file."""
    ensure_config_dir()
    config = {
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri
    }
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)
    console.print(f"[green]Configuration saved to {CONFIG_FILE}[/green]")

def run_setup():
    """Interactive setup process."""
    console.print("[bold cyan]SpotiStats Setup[/bold cyan]")
    console.print("Please enter your Spotify App credentials.")
    console.print("You can get these from https://developer.spotify.com/dashboard")

    client_id = console.input("[yellow]Enter Client ID:[/yellow] ").strip()
    client_secret = console.input("[yellow]Enter Client Secret:[/yellow] ").strip()
    redirect_uri = console.input("[yellow]Enter Redirect URI (default: http://localhost:8888/callback):[/yellow] ").strip()

    if not redirect_uri:
        redirect_uri = "http://localhost:8888/callback"

    if not client_id or not client_secret:
        console.print("[bold red]Error: Client ID and Client Secret are required![/bold red]")
        sys.exit(1)

    save_config(client_id, client_secret, redirect_uri)

def get_spotify_client(config):
    """Initializes and returns the Spotipy client."""
    scope = "user-top-read user-read-private"
    
    auth_manager = SpotifyOAuth(
        client_id=config['client_id'],
        client_secret=config['client_secret'],
        redirect_uri=config['redirect_uri'],
        scope=scope,
        cache_path=str(CACHE_FILE),
        open_browser=True
    )
    
    return spotipy.Spotify(auth_manager=auth_manager)

def main():
    parser = argparse.ArgumentParser(description="SpotiStats: A CLI for your Spotify statistics.")
    parser.add_argument("--global", action="store_true", dest="global_stats", help="Show all-time statistics (default: last month)")
    parser.add_argument("--setup", action="store_true", help="Run initial configuration setup")

    args = parser.parse_args()

    # --- SETUP MODE ---
    if args.setup:
        run_setup()
        return

    # --- VALIDATION ---
    config = load_config()
    if not config:
        console.print("[bold red]Error: Configuration not found.[/bold red]")
        console.print("Please run: [yellow]spotiStats --setup[/yellow]")
        sys.exit(1)

    # --- MAIN LOGIC ---
    try:
        sp = get_spotify_client(config)
        
        # Determine time range
        time_range = 'long_term' if args.global_stats else 'short_term'
        period_label = "All Time" if args.global_stats else "Last Month"

        with console.status("[bold green]Fetching your Spotify stats...[/bold green]"):
            user_data = sp.current_user()
            top_artists = sp.current_user_top_artists(limit=5, time_range=time_range)
            top_tracks = sp.current_user_top_tracks(limit=5, time_range=time_range)

        # --- RENDER UI ---
        ui.display_dashboard(user_data, top_artists, top_tracks, period_label)

    except spotipy.exceptions.SpotifyException as e:
        console.print(f"[bold red]Spotify API Error:[/bold red] {e}")
    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred:[/bold red] {e}")

if __name__ == "__main__":
    main()
