# pygames

2 video-game catalog bulk harvesters grouped onto the
[harvestkit](https://github.com/LeMetadatarr/harvestkit) resumable-harvest
engine. Extracted from [metadatarr](https://github.com/TigreGotico/metadatarr)'s
scraper collection into its own standalone package.

## Sources

| Scraper | Registry name | Source |
| --- | --- | --- |
| `steam_games` | `steam_games` | SteamSpy full catalog |
| `rawg_games` | `rawg_games` | RAWG games database (requires `RAWG_KEY`) |

## Install

```bash
pip install pygames
# or, for the HuggingFace publisher (via harvestkit):
pip install "pygames[hf]"
# or, for Cloudflare-guarded sources:
pip install "pygames[stealth]"
```

## Usage

```bash
# list every registered scraper
pygames-harvest --list

# harvest one source (resumable — safe to Ctrl-C and rerun)
pygames-harvest steam_games --output ~/.cache/metadatarr/scrapers/
```

Every scraper is a `harvestkit.engine.Source` subclass: checkpoint/dedup/
pagination/throttle are handled by the shared engine, each module only
answers `initial_cursor()` and `fetch(cursor)`. See
[harvestkit](https://github.com/LeMetadatarr/harvestkit) for the full engine
API.

## License

Apache-2.0
