# VLRRatingCalculatorDB

Database helper module for the [VLR Scrapper](https://www.vlr.gg) project. Provides
SQLAlchemy ORM models, Pydantic DTOs, and a high-level `DBHelper` class for storing
scraped Valorant match, map, and player statistics.

> Version: **0.1.0** · Python: **≥ 3.14** · License: private/unlicensed

---

## Features

- **SQLAlchemy 2.0** ORM models with a typed declarative base (`Base`).
- **Pydantic v2** DTOs for request/response validation around the persistence layer.
- `DBHelper` — single entry point that wires up the engine, creates the schema, and
  exposes idempotent add operations for matches, maps, and player stats.
- Idempotent inserts: re-adding a match (by `link`) or a map (by
  `match_id` + `map_id`) returns `"… already exists"` instead of raising.

---

## Project layout

```
VLRRatingCalculatorDB/
├── pyproject.toml
├── README.md
└── src/
    └── VLRRatingCalculatorDB/
        ├── __init__.py            # Public re-exports
        ├── db_helper.py           # DBHelper class (engine + CRUD)
        ├── model/                 # SQLAlchemy ORM models
        │   ├── base.py            # DeclarativeBase
        │   ├── match.py           # val_matches
        │   ├── map.py             # val_maps
        │   └── player.py          # val_players
        └── dto/                   # Pydantic schemas (Input / DTO / Output)
            ├── match_info.py
            ├── map_info.py
            └── player_stats.py
```

---

## Installation

This project ships as a `src/`-layout package and is meant to be installed
editable from the repository root:

Dependencies (declared in `pyproject.toml`):

| Package      | Version  |
| ------------ | -------- |
| `sqlalchemy` | `>= 2.0` |
| `pydantic`   | `>= 2.0` |

---

## Public API

Re-exported from `VLRRatingCalculatorDB`:

```python
from VLRRatingCalculatorDB import (
    Base,
    DBHelper,
    MapModel,
    MatchModel,
    PlayerModel,
)
```

### ORM models

| Model         | Table         | Key columns                                                                |
| ------------- | ------------- | -------------------------------------------------------------------------- |
| `MatchModel`  | `val_matches` | `id`, `vlr_match_id` (unique), `link`                                      |
| `MapModel`    | `val_maps`    | `id`, `match_id` (FK → `val_matches.id`), `map_id`, names, scores, winners |
| `PlayerModel` | `val_players` | `id`, `match_id` (FK), `map_id` (FK → `val_maps.id`), name, agent, stats   |

### DTOs

Each entity has three Pydantic models:

- `XInput` — payload accepted for inserts (no `id`).
- `XDTO` — full representation returned to consumers (with `id`).
- `XOutput`— wrapper for a list of `XDTO` (e.g. `matches: list[MatchDTO]`).

Entities: `MatchInput/MatchDTO/MatchOutput`, `MapInput/MapDTO/MapOutput`,
`PlayerInput/PlayerDTO/PlayerOutput`.

### `DBHelper`

```python
from VLRRatingCalculatorDB import DBHelper

db = DBHelper("sqlite:///vlr.db")
db.create_data_base()      # create_all() on Base.metadata
db.create_session()        # bind sessionmaker to the engine

status = db.add_match({"vlr_match_id": 12345, "link": "https://www.vlr.gg/..."})
# {"status": "Match added successfully", "match_id": 1}
# or
# {"status": "Match already exists"}

db.add_map({...})          # checks (match_id, map_id) uniqueness
db.add_player({...})       # always inserts
```

Available methods:

- `create_data_base()` — create all tables.
- `create_session()` — build the `sessionmaker` and assign it to `self.Session`.
- `add_match(match_dict)` — insert unless `link` already exists.
- `add_map(map_dict)` — insert unless the `(match_id, map_id)` pair exists.
- `add_player(player_dict)` — insert a single player stats row.

> **Note:** `add_match`/`add_map` call `self.Session` directly, so `create_session()`
> must run before any insert.

---

## Schema

```text
val_matches  ─┬─< val_maps ──< val_players
              └────────────────< val_players
```

- One match → many maps.
- One map → many player rows (one per player per side).
- A player row references both its parent `match_id` and `map_id` for ergonomic joins.

---
