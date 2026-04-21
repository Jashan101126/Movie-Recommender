import requests
import streamlit as st

# =============================
# CONFIG
# =============================
API_BASE = "https://movie-rec-466x.onrender.com" or "http://127.0.0.1:8000"
TMDB_IMG = "https://image.tmdb.org/t/p/w500"

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# =============================
# STYLES
# =============================
st.markdown(
    """
<style>
header[data-testid="stHeader"] {
    display: none !important;
}
div[data-testid="stToolbar"] {
    display: none !important;
}
.block-container {
    padding-top: 0.6rem !important;
    padding-bottom: 2rem;
    max-width: 1450px;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(59,130,246,0.14), transparent 28%),
        radial-gradient(circle at top right, rgba(239,68,68,0.12), transparent 25%),
        linear-gradient(180deg, #050b18 0%, #0b1220 45%, #111827 100%);
    color: white;
}

.main-title {
    font-size: 3.3rem;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 0.25rem;
    letter-spacing: -0.02em;
}
.small-muted {
    color: #d1d5db;
    font-size: 1rem;
    line-height: 1.5;
}
.section-heading {
    color: #ffffff;
    font-size: 2rem;
    font-weight: 800;
    margin-top: 0.5rem;
    margin-bottom: 1rem;
}
.movie-title {
    font-size: 0.96rem;
    line-height: 1.22rem;
    min-height: 2.45rem;
    max-height: 2.45rem;
    overflow: hidden;
    font-weight: 700;
    color: #ffffff;
    margin-top: 0.55rem;
    text-align: center;
}
.label-title {
    color: #f3f4f6;
    font-weight: 700;
    font-size: 1rem;
    margin-bottom: 0.35rem;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(8,15,28,0.98), rgba(13,20,34,0.98)) !important;
    border-right: 1px solid rgba(255,255,255,0.06);
}
section[data-testid="stSidebar"] .block-container {
    padding-top: 1.2rem !important;
}
.sidebar-title {
    color: #ffffff;
    font-weight: 800;
    font-size: 1.35rem;
    margin-bottom: 0.6rem;
}
.sidebar-sub {
    color: #e5e7eb;
    font-size: 1rem;
    font-weight: 700;
    margin-top: 1.2rem;
    margin-bottom: 0.55rem;
}

div[data-baseweb="select"] > div {
    background: rgba(17,24,39,0.9) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    border-radius: 14px !important;
    min-height: 48px;
}
.stTextInput input {
    background: rgba(10,17,30,0.95) !important;
    color: #ffffff !important;
    border: 1px solid rgba(255,255,255,0.14) !important;
    border-radius: 14px !important;
    min-height: 52px;
    font-size: 1rem !important;
}
.stTextInput input::placeholder {
    color: #9ca3af !important;
    opacity: 1 !important;
}

.stButton > button {
    width: 100%;
    border-radius: 14px;
    border: none;
    color: white;
    font-weight: 700;
    background: linear-gradient(90deg, #ef4444, #dc2626);
    padding: 0.7rem 0.95rem;
    box-shadow: 0 8px 22px rgba(239,68,68,0.28);
}
.stButton > button:hover {
    background: linear-gradient(90deg, #dc2626, #b91c1c);
    color: white;
    transform: translateY(-1px);
}

.card {
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 18px;
    background: rgba(17,24,39,0.72);
    backdrop-filter: blur(8px);
    box-shadow: 0 14px 35px rgba(0,0,0,0.22);
}

.poster-link {
    display: block;
    text-decoration: none !important;
    margin: 0;
    padding: 0;
}

.poster-card {
    position: relative;
    border-radius: 18px;
    overflow: hidden;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 10px 26px rgba(0,0,0,0.24);
    transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
    margin: 0;
    padding: 0;
}

.poster-card:hover {
    transform: translateY(-8px) scale(1.025);
    box-shadow: 0 18px 42px rgba(0,0,0,0.34), 0 0 22px rgba(239,68,68,0.16);
    border-color: rgba(239,68,68,0.55);
}

.poster-card img {
    display: block !important;
    width: 100%;
    margin: 0 !important;
    padding: 0 !important;
    border: none !important;
    vertical-align: middle;
}

.poster-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(to top, rgba(0,0,0,0.28), rgba(0,0,0,0.02) 55%, rgba(0,0,0,0.00));
    opacity: 0;
    transition: opacity 0.22s ease;
    display: flex;
    align-items: flex-end;
    justify-content: center;
    padding-bottom: 12px;
}

.poster-card:hover .poster-overlay {
    opacity: 1;
}

.poster-overlay span {
    background: rgba(239,68,68,0.92);
    color: white;
    font-weight: 700;
    font-size: 0.85rem;
    padding: 6px 12px;
    border-radius: 999px;
    backdrop-filter: blur(4px);
}

.poster-fallback {
    width: 100%;
    aspect-ratio: 2 / 3;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 18px;
    background: rgba(255,255,255,0.04);
    color: #f3f4f6;
    font-weight: 700;
    margin: 0;
    padding: 0;
}

hr {
    border-color: rgba(255,255,255,0.08);
}

label, .stSelectbox label, .stTextInput label {
    color: #f3f4f6 !important;
    font-weight: 700 !important;
    opacity: 1 !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# =============================
# STATE + ROUTING
# =============================
if "view" not in st.session_state:
    st.session_state.view = "home"
if "selected_tmdb_id" not in st.session_state:
    st.session_state.selected_tmdb_id = None

qp_view = st.query_params.get("view")
qp_id = st.query_params.get("id")
if qp_view in ("home", "details"):
    st.session_state.view = qp_view
if qp_id:
    try:
        st.session_state.selected_tmdb_id = int(qp_id)
        st.session_state.view = "details"
    except Exception:
        pass


def goto_home():
    st.session_state.view = "home"
    st.query_params["view"] = "home"
    if "id" in st.query_params:
        del st.query_params["id"]
    st.rerun()


def goto_details(tmdb_id: int):
    st.session_state.view = "details"
    st.session_state.selected_tmdb_id = int(tmdb_id)
    st.query_params["view"] = "details"
    st.query_params["id"] = str(int(tmdb_id))
    st.rerun()


# =============================
# API HELPERS
# =============================
@st.cache_data(ttl=30)
def api_get_json(path: str, params: dict | None = None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=25)
        if r.status_code >= 400:
            return None, f"HTTP {r.status_code}: {r.text[:300]}"
        return r.json(), None
    except Exception as e:
        return None, f"Request failed: {e}"


def to_cards_from_tfidf_items(tfidf_items):
    cards = []
    for x in tfidf_items or []:
        tmdb = x.get("tmdb") or {}
        if tmdb.get("tmdb_id"):
            cards.append(
                {
                    "tmdb_id": tmdb["tmdb_id"],
                    "title": tmdb.get("title") or x.get("title") or "Untitled",
                    "poster_url": tmdb.get("poster_url"),
                }
            )
    return cards


def parse_tmdb_search_to_cards(data, keyword: str, limit: int = 24):
    keyword_l = keyword.strip().lower()

    if isinstance(data, dict) and "results" in data:
        raw = data.get("results") or []
        raw_items = []
        for m in raw:
            title = (m.get("title") or "").strip()
            tmdb_id = m.get("id")
            poster_path = m.get("poster_path")
            if not title or not tmdb_id:
                continue
            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": f"{TMDB_IMG}{poster_path}" if poster_path else None,
                    "release_date": m.get("release_date", ""),
                }
            )

    elif isinstance(data, list):
        raw_items = []
        for m in data:
            tmdb_id = m.get("tmdb_id") or m.get("id")
            title = (m.get("title") or "").strip()
            poster_url = m.get("poster_url")
            if not title or not tmdb_id:
                continue
            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": poster_url,
                    "release_date": m.get("release_date", ""),
                }
            )
    else:
        return [], []

    matched = [x for x in raw_items if keyword_l in x["title"].lower()]
    final_list = matched if matched else raw_items

    suggestions = []
    for x in final_list[:10]:
        year = (x.get("release_date") or "")[:4]
        label = f"{x['title']} ({year})" if year else x["title"]
        suggestions.append((label, x["tmdb_id"]))

    cards = [
        {"tmdb_id": x["tmdb_id"], "title": x["title"], "poster_url": x["poster_url"]}
        for x in final_list[:limit]
    ]
    return suggestions, cards


def poster_grid(cards, cols=6, key_prefix="grid"):
    if not cards:
        st.info("No movies to show.")
        return

    rows = (len(cards) + cols - 1) // cols
    idx = 0

    for r in range(rows):
        colset = st.columns(cols)

        for c in range(cols):
            if idx >= len(cards):
                break

            m = cards[idx]
            idx += 1

            tmdb_id = m.get("tmdb_id")
            title = m.get("title", "Untitled")
            poster = m.get("poster_url")

            with colset[c]:
                if tmdb_id:
                    target_href = f"?view=details&id={tmdb_id}"
                    if poster:
                        st.markdown(
                            f"""
                            <a class="poster-link" href="{target_href}" target="_self">
                                <div class="poster-card">
                                    <img src="{poster}" alt="{title}">
                                    <div class="poster-overlay"><span>View Details</span></div>
                                </div>
                            </a>
                            """,
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            f"""
                            <a class="poster-link" href="{target_href}" target="_self">
                                <div class="poster-card">
                                    <div class="poster-fallback">No poster</div>
                                    <div class="poster-overlay"><span>View Details</span></div>
                                </div>
                            </a>
                            """,
                            unsafe_allow_html=True,
                        )
                else:
                    st.markdown(
                        "<div class='poster-card'><div class='poster-fallback'>No poster</div></div>",
                        unsafe_allow_html=True,
                    )

                st.markdown(
                    f"<div class='movie-title'>{title}</div>",
                    unsafe_allow_html=True,
                )


# =============================
# SIDEBAR
# =============================
with st.sidebar:
    st.markdown("<div class='sidebar-title'>🎬 Menu</div>", unsafe_allow_html=True)
    if st.button("🏠 Home"):
        goto_home()

    st.markdown("---")
    st.markdown("<div class='sidebar-sub'>🏠 Home Feed</div>", unsafe_allow_html=True)

    category_map = {
        "Trending": "trending",
        "Popular": "popular",
        "Top Rated": "top_rated",
        "Now Playing": "now_playing",
        "Upcoming": "upcoming",
    }

    selected_display = st.selectbox(
        "Category",
        list(category_map.keys()),
        index=0,
    )
    home_category = category_map[selected_display]

    grid_cols = st.slider("Grid columns", 4, 8, 6)

# =============================
# HEADER
# =============================
st.markdown("<div class='main-title'>🎬 Movie Recommender</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='small-muted'>Type keyword → dropdown suggestions + matching results → open → details + recommendations</div>",
    unsafe_allow_html=True,
)
st.divider()

# ==========================================================
# VIEW: HOME
# ==========================================================
if st.session_state.view == "home":
    st.markdown("<div class='label-title'>Search by movie title</div>", unsafe_allow_html=True)
    typed = st.text_input("")

    st.divider()

    if typed.strip():
        if len(typed.strip()) < 2:
            st.caption("Type at least 2 characters for suggestions.")
        else:
            data, err = api_get_json("/tmdb/search", params={"query": typed.strip()})

            if err or data is None:
                st.error(f"Search failed: {err}")
            else:
                suggestions, cards = parse_tmdb_search_to_cards(
                    data, typed.strip(), limit=24
                )

                if suggestions:
                    st.markdown("<div class='label-title'>Suggestions</div>", unsafe_allow_html=True)
                    labels = ["-- Select a movie --"] + [s[0] for s in suggestions]
                    selected = st.selectbox("", labels, index=0)

                    if selected != "-- Select a movie --":
                        label_to_id = {s[0]: s[1] for s in suggestions}
                        goto_details(label_to_id[selected])
                else:
                    st.info("No suggestions found. Try another keyword.")

                st.markdown("<div class='section-heading'>Results</div>", unsafe_allow_html=True)
                poster_grid(cards, cols=grid_cols, key_prefix="search_results")

        st.stop()

    st.markdown(
        f"<div class='section-heading'>🏠 Home — {selected_display}</div>",
        unsafe_allow_html=True,
    )

    home_cards, err = api_get_json(
        "/home", params={"category": home_category, "limit": 24}
    )
    if err or not home_cards:
        st.error(f"Home feed failed: {err or 'Unknown error'}")
        st.stop()

    poster_grid(home_cards, cols=grid_cols, key_prefix="home_feed")

# ==========================================================
# VIEW: DETAILS
# ==========================================================
elif st.session_state.view == "details":
    tmdb_id = st.session_state.selected_tmdb_id
    if not tmdb_id:
        st.warning("No movie selected.")
        if st.button("← Back to Home"):
            goto_home()
        st.stop()

    a, b = st.columns([3, 1])
    with a:
        st.markdown("<div class='section-heading'>📄 Movie Details</div>", unsafe_allow_html=True)
    with b:
        if st.button("← Back to Home"):
            goto_home()

    data, err = api_get_json(f"/movie/id/{tmdb_id}")
    if err or not data:
        st.error(f"Could not load details: {err or 'Unknown error'}")
        st.stop()

    left, right = st.columns([1, 2.4], gap="large")

    with left:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        if data.get("poster_url"):
            st.image(data["poster_url"], use_container_width=True)
        else:
            st.write("🖼️ No poster")
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"## {data.get('title','')}")
        release = data.get("release_date") or "-"
        genres = ", ".join([g["name"] for g in data.get("genres", [])]) or "-"
        st.markdown(
            f"<div class='small-muted'><b>Release:</b> {release}</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div class='small-muted'><b>Genres:</b> {genres}</div>",
            unsafe_allow_html=True,
        )
        st.markdown("---")
        st.markdown("### Overview")
        st.write(data.get("overview") or "No overview available.")
        st.markdown("</div>", unsafe_allow_html=True)

    if data.get("backdrop_url"):
        st.markdown("<div class='section-heading'>Backdrop</div>", unsafe_allow_html=True)
        st.image(data["backdrop_url"], use_container_width=True)

    st.divider()
    st.markdown("<div class='section-heading'>✅ Recommendations</div>", unsafe_allow_html=True)

    title = (data.get("title") or "").strip()
    if title:
        bundle, err2 = api_get_json(
            "/movie/search",
            params={"query": title, "tfidf_top_n": 12, "genre_limit": 12},
        )

        if not err2 and bundle:
            st.markdown("<div class='label-title'>🔎 Similar Movies (TF-IDF)</div>", unsafe_allow_html=True)
            poster_grid(
                to_cards_from_tfidf_items(bundle.get("tfidf_recommendations")),
                cols=grid_cols,
                key_prefix="details_tfidf",
            )

            st.markdown("<div class='label-title' style='margin-top:1.2rem;'>🎭 More Like This (Genre)</div>", unsafe_allow_html=True)
            poster_grid(
                bundle.get("genre_recommendations", []),
                cols=grid_cols,
                key_prefix="details_genre",
            )
        else:
            st.info("Showing Genre recommendations (fallback).")
            genre_only, err3 = api_get_json(
                "/recommend/genre", params={"tmdb_id": tmdb_id, "limit": 18}
            )
            if not err3 and genre_only:
                poster_grid(
                    genre_only, cols=grid_cols, key_prefix="details_genre_fallback"
                )
            else:
                st.warning("No recommendations available right now.")
    else:
        st.warning("No title available to compute recommendations.")