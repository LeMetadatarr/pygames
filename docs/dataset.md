# Dataset

This repo produces two video-game datasets:

- `steam_games`: the full Steam catalog via SteamSpy, with optional enrichment from the Steam store API.
- `rawg_games`: the RAWG games database.

One row represents one game.

## Format

### `steam_games.jsonl`

Each line is a flat JSON object with these fields:

| Field | Type | Description |
| --- | --- | --- |
| `steam_appid` | integer | Steam application ID |
| `name` | string or null | Game name |
| `developer` | string or null | Developer |
| `publisher` | string or null | Publisher |
| `score_rank` | integer or null | Score rank |
| `positive_reviews` | integer or null | Number of positive reviews |
| `negative_reviews` | integer or null | Number of negative reviews |
| `owners` | string or null | Estimated owner range |
| `average_playtime_forever` | integer or null | Average playtime in minutes, all time |
| `average_playtime_2weeks` | integer or null | Average playtime in minutes, last two weeks |
| `median_playtime_forever` | integer or null | Median playtime in minutes, all time |
| `price_usd` | float or null | Price in US dollars |
| `discount_pct` | string or null | Discount percentage |
| `ccu` | integer or null | Concurrent users |
| `type` | string or null | Steam store type, set when `--enrich` is used |
| `genres` | list of strings | Genres, set when `--enrich` is used |
| `categories` | list of strings | Categories, set when `--enrich` is used |
| `release_date` | string or null | Release date, set when `--enrich` is used |
| `is_free` | boolean or null | Free-to-play flag, set when `--enrich` is used |
| `platforms_windows` | boolean or null | Windows support, set when `--enrich` is used |
| `platforms_mac` | boolean or null | macOS support, set when `--enrich` is used |
| `platforms_linux` | boolean or null | Linux support, set when `--enrich` is used |
| `metacritic_score` | integer or null | Metacritic score, set when `--enrich` is used |
| `short_description` | string or null | Short description, set when `--enrich` is used |

### `rawg_games.jsonl`

Each line is a flat JSON object with these fields:

| Field | Type | Description |
| --- | --- | --- |
| `rawg_id` | integer | RAWG game ID |
| `slug` | string or null | RAWG slug |
| `name` | string or null | Game name |
| `released` | string or null | Release date |
| `metacritic` | integer or null | Metacritic score |
| `rating` | float or null | RAWG user rating |
| `rating_top` | integer or null | Rating scale top |
| `ratings_count` | integer or null | Number of ratings |
| `esrb_rating` | string or null | ESRB rating |
| `genres` | list of strings | Genres |
| `platforms` | list of strings | Platforms |
| `tags` | list of strings | English tags |
| `stores` | list of strings | Stores |
| `developers` | list of strings | Developers |
| `publishers` | list of strings | Publishers |
| `background_image` | string or null | Background image URL |
| `entity_type` | string | Constant value `video_game` |

## How to generate

Install the package:

```bash
pip install pygames
```

Harvest Steam games:

```bash
pygames-harvest steam_games --output ~/.cache/metadatarr/scrapers/
```

With Steam store enrichment:

```bash
pygames-harvest steam_games --enrich --output ~/.cache/metadatarr/scrapers/
```

Harvest RAWG games:

```bash
RAWG_KEY=xxx pygames-harvest rawg_games --output ~/.cache/metadatarr/scrapers/
```

Python equivalent:

```python
from pathlib import Path
from pygames.harvest.steam_games import SteamGamesSource
from pygames.harvest.rawg_games import RAWGGamesSource

SteamGamesSource().run(Path.home() / ".cache/metadatarr/scrapers")
RAWGGamesSource().run(Path.home() / ".cache/metadatarr/scrapers")
```

## Publish on Hugging Face

Yes. Both datasets are structured video-game catalogs with genres, platforms, release dates, and review signals. They are useful for game-discovery, recommendation, and classification research. Confirm that redistribution of SteamSpy and RAWG data complies with their respective terms of service.

## ML tasks served

- Game genre and tag classification.
- Game recommendation systems.
- Review-sentiment proxy modeling from positive/negative counts.
- Release-date and platform-support prediction.
- Cross-store entity linking between Steam and RAWG.
