# GeoMap - Tactical 3D Map Command Center

A futuristic, sci-fi themed tactical 3D map interface built with MapLibre GL JS and MapTiler. 
Features high-resolution 3D terrain draped with satellite imagery and a responsive, neon-accented dark mode UI.

## Getting Started

To run this application, you must provide your own MapTiler API key.

1. Clone the repository.
2. Create a `.env` file in the root directory.
3. Add your MapTiler API key to the `.env` file like this:
   ```env
   apiKey=YOUR_MAPTILER_API_KEY
   ```
4. *Important:* Since this is a static HTML/JS project without a bundler, the `.env` file is meant for local use and secret management if you upgrade to a Node.js backend or bundler (like Vite) later. For now, you must manually insert your key into the `index.html` file before running (do not commit your key!).

### Running locally
You can serve the directory using a simple local web server, for example:
```bash
python3 -m http.server 8085
```
Then navigate to `http://localhost:8085` in your browser.

## Acknowledgements
The core mapping logic, API integration, and project architecture were written by myself. The futuristic UI layout, CSS styling, and neon aesthetics were generated with the assistance of AI.
