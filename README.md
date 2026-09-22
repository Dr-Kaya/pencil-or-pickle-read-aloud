# Pencil or Pickle? — Read & Listen

An illustrated book about how AI learns and why it needs us. Read the original pages, hear page-by-page narration, jump between six chapters, adjust reading speed, or download a narrated EPUB.

The original pages remain still. Reading starts only when a visitor presses **Read aloud**. Automatic reading pauses at each chapter’s activities.

## Publishing

The GitHub Actions workflow builds and deploys this reader to GitHub Pages. In repository **Settings → Pages**, select **GitHub Actions** as the publishing source.

The `assets` archives contain the original page images and finished MP3 recordings. They are grouped into small files for reliable upload. The build extracts these files and creates the full-book and chapter EPUB downloads. It does not call any voice API or require secrets, API keys, or a paid service.

To build locally, run `python3 scripts/build_site.py _site` and serve the `_site` folder with any static web server.

## Credits

Text: The DCoaD Literacies Lab and Friends. Book copyright © 2026 Amy Hutchison, Brittany Adams, Kristie Gutierrez, and Erdogan Kaya. Illustrations and book design © 2026 Rebeca J. Pintos. Original acknowledgments and contributor pages are preserved.

Read-aloud recordings were generated with ElevenLabs. Adult voices perform the student roles. This public repository does not grant a new license to the book, illustrations, font, or recordings; the original rights remain with their holders.
