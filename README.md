# 🎵 SpotiStats CLI

**SpotiStats** is a stylish Neofetch-inspired Command Line Interface (CLI) to visualize your Spotify listening habits. Get your top artists and tracks directly in your terminal with a clean, side-by-side layout.

![SpotiStats Preview](https://via.placeholder.com/800x400?text=SpotiStats+CLI+Preview+Placeholder)

## 🚀 Features

- **Neofetch Style:** Beautiful ASCII art logo and organized stats.
- **Short Term Stats:** View your top 5 artists and tracks from the last month (default).
- **Global Stats:** Use the `--global` flag to see your all-time favorites.
- **Interactive Setup:** Easy configuration for your Spotify Developer credentials.
- **Rich Terminal UI:** Powered by the `rich` library for colors and layouts.

---

## 📋 Prerequisites

Before installing, you need a **Spotify Developer Account**.

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).
2. Create a new App (e.g., "SpotiStats CLI").
3. Set the **Redirect URI** to `http://localhost:8888/callback` (or your preferred URI).
4. Note down your **Client ID** and **Client Secret**.

---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/spotiStatsCLI.git
cd spotiStatsCLI
```

### 2. Set up a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install the package
```bash
pip install -e .
```

---

## 🛠 Usage

### Initial Setup
The first time you use the app, you must configure your credentials:
```bash
spotiStats --setup
```
This will prompt you for your `Client ID`, `Client Secret`, and `Redirect URI`. These are saved locally in `~/.config/spotistats/config.json`.

### View Monthly Stats (Default)
To see your stats from the **last 4 weeks**:
```bash
spotiStats
```

### View All-Time Stats
To see your **long-term** (several years) statistics:
```bash
spotiStats --global
```

---

## 📂 Project Structure

- `spotistats/main.py`: Core logic, authentication, and CLI argument handling.
- `spotistats/ui.py`: Visual rendering, ASCII art, and layout.
- `setup.py`: Package installation and entry point definition.

## 🤝 Contributing

Feel free to open issues or submit pull requests to improve the CLI!

## 📄 License

MIT License - See the [LICENSE](LICENSE) file for details.
