# VLRRatingCalculatorDB

Database helper module for the [VLR Scrapper](https://www.vlr.gg) project. Provides
SQLAlchemy ORM models, Pydantic DTOs, and a high-level `DBHelper` class for storing
scraped Valorant match, map, and player statistics.

> Version: **0.2.0** · Python: **≥ 3.10** · License: private/unlicensed

---

## Features

- **SQLAlchemy 2.0** ORM models with a typed declarative base (`Base`).
- **Pydantic v2** DTOs for request/response validation around the persistence layer.
- `DBHelper` — single entry point that wires up the engine, creates the schema, and
  exposes idempotent add operations for matches, maps, and player stats.
- Idempotent inserts: re-adding a match (by `link`) or a map (by
  `vlr_match_id` + `map_id`) returns `"… already exists"` instead of raising.

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

Install directly from the GitHub repository:

```bash
pip install git+https://github.com/matiteus/VLRRatingCalculatorDB
```

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

| Model         | Table         | Key columns                                                                                                                |
| ------------- | ------------- | -------------------------------------------------------------------------------------------------------------------------- |
| `MatchModel`  | `val_matches` | `id`, `vlr_match_id` (unique), `link`                                                                                      |
| `MapModel`    | `val_maps`    | `id`, `db_match_id` (FK → `val_matches.id`), `vlr_match_id`, `map_id`, names, scores, winners                              |
| `PlayerModel` | `val_players` | `id`, `db_match_id` (FK → `val_matches.id`), `map_id` (FK → `val_maps.id`), `name`, `team`, `agent`, `side`, full stat set |

`PlayerModel` exposes the full per-side stat set: `rating`, `acs`, `kills`, `deaths`,
`assists`, `kd_diff`, `kast`, `adr`, `hs`, `fb`, `fd`, `fk_diff`. Note that `kast`
and `hs` are stored as strings (e.g. `"75%"`) because that is the raw representation
scraped from VLR.

### DTOs

Each entity has three Pydantic models:

- `XInput` — payload accepted for inserts (no `id`).
- `XDTO` — full representation returned to consumers (with `id`).
- `XOutput` — wrapper for a list of `XDTO` (e.g. `matches: list[MatchDTO]`).

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

db.add_map({...})          # checks (vlr_match_id, map_id) uniqueness
db.add_player({...})       # always inserts
```

Available methods:

- `create_data_base()` — create all tables.
- `create_session()` — build the `sessionmaker` and assign it to `self.session`.
- `check_if_match_exists(match_link)` — `True` if a match with the given `link` exists.
- `get_match_id(match_link)` — primary key of a match, looked up by `link`.
- `get_map_id(vlr_match_id, map_id)` — primary key of a map, looked up by
  `(vlr_match_id, map_id)`.
- `check_if_map_exists(vlr_match_id, map_id)` — `True` if the composite key exists.
- `add_match(match_dict)` — insert unless `link` already exists.
- `add_map(map_dict)` — insert unless the `(vlr_match_id, map_id)` pair exists.
- `add_player(player_dict)` — insert a single player stats row.
- `close_session()` — close the active session, if one is open.

> **Note:** every method that touches the session (`check_if_*`, `get_*`, `add_*`)
> calls `self.session` directly, so `create_session()` must run first.

---

## Schema

```text
val_matches  ─┬─< val_maps ──< val_players
              └────────────────< val_players
```

- One match → many maps.
- One map → many player rows (one per player per side — the scraper emits
  `both`, `t`, and `ct` rows for each player).
- A player row references both its parent `db_match_id` and `map_id` for ergonomic joins.
