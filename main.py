```python
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    layout="wide"
)

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 장르가 여러 개이면 첫 번째 장르만 사용
    df["장르"] = (
        df["genre"]
        .fillna("알 수 없음")
        .astype(str)
        .str.split("|")
        .str[0]
    )

    # 국가가 여러 개이면 첫 번째 국가만 사용
    df["대표국가"] = (
        df["nation"]
        .fillna("알 수 없음")
        .astype(str)
        .str.split("|")
        .str[0]
    )

    # 숫자형 데이터 변환
    for col in ["total_audi", "first_scrn", "first_week_audi"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # 영화명이 없는 행 제거
    df = df.dropna(subset=["movieNm"])

    return df


df = load_data()


# =====================================================
# 그래프 1. 장르별 영화 편수
# =====================================================

st.header("1. 장르별 영화 편수 (도넛)")

genre_count = df["장르"].value_counts().reset_index()
genre_count.columns = ["장르", "편수"]

fig1 = px.pie(
    genre_count,
    names="장르",
    values="편수",
    hole=0.45
)

fig1.update_traces(
    hovertemplate="%{label}<br>%{value}편 (%{percent})<extra></extra>"
)

st.plotly_chart(fig1, width="stretch")

st.text_input(
    "이 그래프로 알 수 있는 것",
    key="note1"
)

st.divider()


# =====================================================
# 그래프 2. 장르 안의 영화
# =====================================================

st.header("2. 장르 안의 영화 (트리맵)")

# 같은 영화가 여러 행에 있을 수 있으므로
# 장르 + 영화명별로 관객수를 먼저 합칩니다.
treemap_df = (
    df.groupby(
        ["장르", "movieNm"],
        as_index=False
    )["total_audi"]
    .sum()
)

treemap_df = treemap_df.dropna(
    subset=["total_audi"]
)

fig2 = px.treemap(
    treemap_df,
    path=["장르", "movieNm"],
    values="total_audi"
)

fig2.update_traces(
    hovertemplate=(
        "장르: %{parent}<br>"
        "영화: %{label}<br>"
        "총 관객: %{value:,}명"
        "<extra></extra>"
    )
)

st.plotly_chart(fig2, width="stretch")

st.caption(
    "이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)"
)


# =====================================================
# 그래프 3. 총 관객의 분포
# =====================================================

st.header("3. 총 관객의 분포 (히스토그램)")

hist_df = df.dropna(
    subset=["total_audi"]
)

fig3 = px.histogram(
    hist_df,
    x="total_audi",
    nbins=40
)

fig3.update_layout(
    xaxis_title="총 관객 수",
    yaxis_title="영화 편수"
)

st.plotly_chart(fig3, width="stretch")

# 100만 명 미만인 영화 수
under_1m = (
    hist_df["total_audi"] < 1_000_000
).sum()

if not hist_df.empty:
    best = hist_df.loc[
        hist_df["total_audi"].idxmax()
    ]

    st.write(
        f"{len(hist_df)}편 가운데 "
        f"{under_1m}편이 100만 명 미만입니다. "
        f"가장 많이 본 영화는 "
        f"{best['movieNm']} "
        f"({best['total_audi']:,.0f}명)입니다."
    )

st.caption(
    "이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)"
)


# =====================================================
# 그래프 4. 개봉일 스크린 수와 총 관객
# =====================================================

st.header("4. 개봉일 스크린 수와 총 관객 (산점도)")

scatter_df = df.dropna(
    subset=[
        "first_scrn",
        "total_audi",
        "장르"
    ]
)

fig4 = px.scatter(
    scatter_df,
    x="first_scrn",
    y="total_audi",
    color="장르",
    hover_name="movieNm"
)

fig4.update_layout(
    xaxis_title="개봉일 스크린 수",
    yaxis_title="총 관객 수"
)

st.plotly_chart(fig4, width="stretch")

st.caption(
    "이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)"
)


# =====================================================
# 그래프 5. 장르별 총 관객
# =====================================================

st.header("5. 장르별 총 관객 (박스플롯)")

genre_counts = df["장르"].value_counts()

# 영화가 10편 이상인 장르만 사용
big_genres = genre_counts[
    genre_counts >= 10
].index

box_df = df[
    df["장르"].isin(big_genres)
].dropna(
    subset=[
        "장르",
        "total_audi"
    ]
)

fig5 = px.box(
    box_df,
    x="장르",
    y="total_audi",
    points="outliers",
    hover_name="movieNm"
)

fig5.update_layout(
    xaxis_title="장르",
    yaxis_title="총 관객 수"
)

st.plotly_chart(fig5, width="stretch")

st.caption(
    "이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)"
)


# =====================================================
# 그래프 6. 첫 주 관객을 점 크기로
# =====================================================

st.header("6. 첫 주 관객을 점 크기로 (버블)")

bubble_df = df.dropna(
    subset=[
        "first_scrn",
        "total_audi",
        "first_week_audi",
        "장르"
    ]
)

bubble_df = bubble_df[
    bubble_df["first_week_audi"] >= 0
]

fig6 = px.scatter(
    bubble_df,
    x="first_scrn",
    y="total_audi",
    color="장르",
    size="first_week_audi",
    size_max=40,
    hover_name="movieNm"
)

fig6.update_layout(
    xaxis_title="개봉일 스크린 수",
    yaxis_title="총 관객 수"
)

st.plotly_chart(fig6, width="stretch")

st.caption(
    "이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)"
)


# =====================================================
# 그래프 7. 국가에서 장르로
# =====================================================

st.header("7. 국가에서 장르로 (선버스트)")

counted = (
    df.groupby(
        ["대표국가", "장르"],
        as_index=False
    )
    .agg(
        편수=("movieNm", "count")
    )
)

fig7 = px.sunburst(
    counted,
    path=["대표국가", "장르"],
    values="편수"
)

fig7.update_traces(
    hovertemplate=(
        "국가: %{parent}<br>"
        "장르: %{label}<br>"
        "영화 편수: %{value}편"
        "<extra></extra>"
    )
)

st.plotly_chart(fig7, width="stretch")

st.caption(
    "이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)"
)
```
