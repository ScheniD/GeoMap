# GeoMap — Tactical 3D Terrain Command Center

A cinematic, sci-fi themed 3D map interface built with **MapLibre GL JS** and **MapTiler**.
Features high-pitch 3D terrain, animated holographic HUD overlays, live mountain webcams, and an interactive panel for all German federal states.

---

## Features

### 🗺️ Map Views
Three selectable map layers, each switchable from the **Operations** dropdown:
| Option | Style |
|---|---|
| **Map layer — Dark** | Dataviz dark theme (default) |
| **Map layer — Satellite** | Aerial satellite imagery |
| **Map layer — Winter** | Winter/snow terrain style |

### ⛰️ Terrain & Navigation
- **3D terrain** with adjustable exaggeration (▲/▼ knob, top-right)
- **Dramatic tilt** — snaps to high-pitch cinematic view
- **Orbit mode** — slow auto-rotation around the current view
- **Fly → North Sea** / **Fly → Germany Overview** — instant navigation presets

### 🏔️ German Peak Browser
Fly directly to any of **23 mountain peaks** across Germany via the *Fly to peak…* dropdown. Grouped by region:
- **Alps** — Zugspitze, Watzmann, Hochkalter, Berchtesgaden, Allgäu
- **Black Forest** — Feldberg, Belchen, Schauinsland
- **Bavarian Forest** — Großer Arber, Großer Rachel, Lusen
- **Harz** — Brocken, Wurmberg, Achtermann
- **Erzgebirge** — Fichtelberg, Keilberg
- **Thuringia / Rhön** — Beerberg, Wasserkuppe, Großer Inselsberg
- **Sauerland** — Langenberg, Kahler Asten
- **Eifel / Hunsrück** — Erbeskopf, Hohe Acht
- **Taunus** — Großer Feldberg

### 📷 Live Mountain Webcams
Selecting a peak that has a verified live camera automatically opens a **floating camera panel** in the bottom-right corner.

| Peak | Camera source |
|---|---|
| Zugspitze | Zugspitze summit — foto-webcam.eu |
| Watzmann | Jenner (Berchtesgaden) — foto-webcam.eu |
| Berchtesgaden Alps | Jenner — foto-webcam.eu |
| Allgäu | Nebelhorn — foto-webcam.eu |
| Feldberg (Black Forest) | Hochblauen — foto-webcam.eu |

The panel:
- Shows only the raw camera image (no website chrome)
- Refreshes automatically every **30 seconds**
- Is **draggable** — grab the header bar to reposition
- Persists across map control changes — only updates when you select a different peak
- Has a **↗ Full feed** link to open the webcam page in a new tab

### 🗾 Federal State Scanner
Click any German federal state on the map to scan it. The sidebar shows:
- Region name, coordinates, peak elevation, area
- Threat level meter (colour-coded)

### 🛰️ HUD Overlays
- Live clock (top)
- Real-time latitude / longitude / zoom (bottom strip)
- Corner bracket overlays for a cinematic tactical look

---

## Running Locally

> **Note:** A custom `server.py` is required to proxy live webcam images (bypasses hotlink protection). You can still use `python3 -m http.server` but webcams will not load.

### With webcam support (recommended)
```bash
python3 server.py
```
Then open `http://localhost:8900`.

### Without webcam support
```bash
python3 -m http.server 8900
```

---

## Setup

1. Clone the repository.
2. Create a `.env` file in the root directory with your MapTiler API key:
   ```env
   apiKey=YOUR_MAPTILER_API_KEY
   ```
3. The API key is embedded directly in `index.html` — do **not** commit your key to a public repo.

---

## Tech Stack
- [MapLibre GL JS](https://maplibre.org/) — WebGL map engine
- [MapTiler](https://www.maptiler.com/) — Tiles, terrain DEM, and styles
- [foto-webcam.eu](https://www.foto-webcam.eu/) — Live mountain webcam images
- Vanilla HTML / CSS / JS — no framework, no build step

## Acknowledgements
Map logic, API integration, and architecture by Dominik. UI design, sci-fi aesthetics, and feature development assisted by AI.
