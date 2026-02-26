from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.columns import Columns
from rich.align import Align

# --- ASCII ART ---
SPOTIFY_ASCII = """
[green]
⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣤⣶⣶⣶⣶⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⡀⠀⠀⠀⠀
⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀
⠀⢀⣾⣿⡿⠿⠛⠛⠛⠉⠉⠉⠉⠛⠛⠛⠿⠿⣿⣿⣿⣿⣿⣷⡀⠀
⠀⣾⣿⣿⣇⠀⣀⣀⣠⣤⣤⣤⣤⣤⣀⣀⠀⠀⠀⠈⠙⠻⣿⣿⣷⠀
⢠⣿⣿⣿⣿⡿⠿⠟⠛⠛⠛⠛⠛⠛⠻⠿⢿⣿⣶⣤⣀⣠⣿⣿⣿⡄
⢸⣿⣿⣿⣿⣇⣀⣀⣤⣤⣤⣤⣤⣄⣀⣀⠀⠀⠉⠛⢿⣿⣿⣿⣿⡇
⠘⣿⣿⣿⣿⣿⠿⠿⠛⠛⠛⠛⠛⠛⠿⠿⣿⣶⣦⣤⣾⣿⣿⣿⣿⠃
⠀⢿⣿⣿⣿⣿⣤⣤⣤⣤⣶⣶⣦⣤⣤⣄⡀⠈⠙⣿⣿⣿⣿⣿⡿⠀
⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣿⣿⣿⣿⡿⠁⠀
⠀⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⠀⠀
⠀⠀⠀⠀⠈⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⠙⠛⠛⠿⠿⠿⠿⠛⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀
[/green]
"""

def create_info_panel(user_data, top_artists, top_tracks, period_label):
    """Generates the right-side panel with user stats."""
    
    # 1. User Header
    user_table = Table.grid(padding=(0, 1))
    user_table.add_column(style="bold white")
    user_table.add_column(style="green")
    
    user_table.add_row("User:", user_data['display_name'])
    user_table.add_row("Followers:", str(user_data['followers']['total']))
    user_table.add_row("Period:", period_label)

    # 2. Top Artists
    artist_table = Table(box=None, padding=(0, 1), show_header=False)
    artist_table.add_column("Rank", style="bold green", justify="right", width=3)
    artist_table.add_column("Artist", style="white")

    for i, artist in enumerate(top_artists['items'], 1):
        artist_table.add_row(f"{i}.", artist['name'])

    # 3. Top Tracks
    track_table = Table(box=None, padding=(0, 1), show_header=False)
    track_table.add_column("Rank", style="bold green", justify="right", width=3)
    track_table.add_column("Track", style="white")

    for i, track in enumerate(top_tracks['items'], 1):
        artist_names = ", ".join([a['name'] for a in track['artists']])
        track_display = f"{track['name']} [dim]({artist_names})[/dim]"
        track_table.add_row(f"{i}.", track_display)

    # Combine into a single layout
    content = Table.grid(padding=(1, 0))
    content.add_row(user_table)
    content.add_row(Text("Top 5 Artists", style="bold green underline"))
    content.add_row(artist_table)
    content.add_row(Text("Top 5 Tracks", style="bold green underline"))
    content.add_row(track_table)

    return content

def display_dashboard(user_data, top_artists, top_tracks, period_label):
    console = Console()
    
    # Create the main table that acts as the split layout
    layout_table = Table(show_header=False, box=None, padding=(0, 4))
    layout_table.add_column("Logo", justify="center", vertical="middle")
    layout_table.add_column("Stats", vertical="top")

    # Left: ASCII Art
    logo_panel = Align.center(Text.from_markup(SPOTIFY_ASCII), vertical="middle")
    
    # Right: Info
    info_panel = create_info_panel(user_data, top_artists, top_tracks, period_label)

    layout_table.add_row(logo_panel, info_panel)
    
    console.print("")
    console.print(layout_table)
    console.print("")
