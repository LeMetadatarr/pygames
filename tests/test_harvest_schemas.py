"""Row-schema equivalence tests for the 2 video-game scrapers.

Relocated verbatim (assertions untouched) from metadatarr's
test_scrapers_batch1.py, keeping only the tests for scrapers that live in
this package, re-pointed at pygames.harvest.*. These lock the exact flat-row
shape each scraper emits (the contract the LeData datasets depend on)
against a realistic upstream sample, so a future engine change can't
silently alter the output schema.
"""
from __future__ import annotations

from harvestkit.engine import all_sources

from pygames.harvest.rawg_games import RAWGGamesSource
from pygames.harvest.steam_games import SteamGamesSource


def test_rawg_games_map_row_schema():
    src = RAWGGamesSource()
    g = {
        "id": 3498,
        "slug": "grand-theft-auto-v",
        "name": "Grand Theft Auto V",
        "released": "2013-09-17",
        "metacritic": 92,
        "rating": 4.47,
        "rating_top": 5,
        "ratings_count": 6500,
        "esrb_rating": {"name": "Mature"},
        "genres": [{"name": "Action"}, {"name": "Adventure"}],
        "platforms": [{"platform": {"name": "PC"}}, {"platform": {"name": "PS5"}}],
        "tags": [{"name": "Singleplayer", "language": "eng"},
                 {"name": "Multijoueur", "language": "fra"}],
        "stores": [{"store": {"name": "Steam"}}],
        "developers": [{"name": "Rockstar North"}],
        "publishers": [{"name": "Rockstar Games"}],
        "background_image": "http://example.com/img.jpg",
    }
    row = src.map_row(g)
    assert row["rawg_id"] == 3498
    assert row["esrb_rating"] == "Mature"
    assert row["genres"] == ["Action", "Adventure"]
    assert row["platforms"] == ["PC", "PS5"]
    assert row["tags"] == ["Singleplayer"]  # only "eng" tags kept
    assert row["stores"] == ["Steam"]
    assert row["entity_type"] == "video_game"
    assert set(row) == {
        "rawg_id", "slug", "name", "released", "metacritic", "rating",
        "rating_top", "ratings_count", "esrb_rating", "genres", "platforms",
        "tags", "stores", "developers", "publishers", "background_image",
        "entity_type",
    }


def test_rawg_games_map_row_drops_records_without_id():
    assert RAWGGamesSource().map_row({"id": None}) is None


def test_rawg_games_fetch_stops_without_next():
    src = RAWGGamesSource()
    src.get_json = lambda url, params: {"results": [{"id": 1}], "next": None}
    rows, cursor = src.fetch(1)
    assert len(rows) == 1
    assert cursor is None


def test_steam_games_map_row_schema():
    src = SteamGamesSource()
    entry = {
        "appid": 620,
        "name": "Portal 2",
        "developer": "Valve",
        "publisher": "Valve",
        "score_rank": "",
        "positive": 1000,
        "negative": 10,
        "owners": "10,000,000 .. 20,000,000",
        "average_forever": 500,
        "average_2weeks": 0,
        "median_forever": 200,
        "price": "999",
        "discount": "0",
        "ccu": 300,
    }
    row = src.map_row("620", entry)
    assert row["steam_appid"] == 620
    assert row["price_usd"] == 9.99
    assert row["score_rank"] is None  # empty string -> None
    assert row["discount_pct"] == "0"  # non-empty string stays truthy
    assert row["genres"] == []  # enrichment not ported, stays empty
    assert set(row) == {
        "steam_appid", "name", "developer", "publisher", "score_rank",
        "positive_reviews", "negative_reviews", "owners",
        "average_playtime_forever", "average_playtime_2weeks",
        "median_playtime_forever", "price_usd", "discount_pct", "ccu",
        "type", "genres", "categories", "release_date", "is_free",
        "platforms_windows", "platforms_mac", "platforms_linux",
        "metacritic_score", "short_description",
    }


def test_steam_games_map_row_appid_fallback():
    row = SteamGamesSource().map_row("99", {"name": "No appid field"})
    assert row["steam_appid"] == 99


def test_steam_games_fetch_stops_on_empty_page():
    src = SteamGamesSource()
    src.get_json = lambda url, params: {}
    rows, cursor = src.fetch(0)
    assert rows == []
    assert cursor is None


def test_steam_enrich_flag_applies_detail(monkeypatch):
    src = SteamGamesSource()
    # simulate --enrich
    import argparse
    src.configure(argparse.Namespace(enrich=True))
    assert src.enrich is True

    # one SteamSpy page + a store-detail stub
    monkeypatch.setattr(SteamGamesSource, "get_json",
                        lambda self, url, params=None: {"10": {"appid": 10, "name": "CS", "price": "0"}}
                        if params.get("page") == 0 else {}, raising=True)
    monkeypatch.setattr(SteamGamesSource, "_fetch_detail",
                        lambda self, appid: {"type": "game", "genres": [{"description": "Action"}],
                                             "is_free": True}, raising=True)
    rows, nxt = src.fetch(0)
    assert rows[0]["type"] == "game"
    assert rows[0]["genres"] == ["Action"]
    assert rows[0]["is_free"] is True


def test_steam_without_enrich_leaves_detail_fields_unset(monkeypatch):
    src = SteamGamesSource()  # enrich defaults False
    monkeypatch.setattr(SteamGamesSource, "get_json",
                        lambda self, url, params=None: {"10": {"appid": 10, "name": "CS", "price": "0"}}
                        if params.get("page") == 0 else {}, raising=True)
    rows, _ = src.fetch(0)
    assert rows[0]["genres"] == []
    assert rows[0]["type"] is None


def test_pygames_scrapers_are_registered():
    reg = all_sources()
    assert reg.get("rawg_games") is RAWGGamesSource
    assert reg.get("steam_games") is SteamGamesSource
