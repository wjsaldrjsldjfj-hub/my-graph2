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
    # 데이터 불러오기
    df = pd.read_csv(DATA_URL)

    # 장르: 여러 장르가 "|"로 연결되어 있으면 첫 번째 장르만 사용
    df["장르"] = (
        df["genre"]
        .fillna("알 수 없음")
        .astype(str)
        .str.split("|")
        .str[0]
    )

    # 국가: 여러 국가가 "|"로 연결되어 있으면 첫 번째 국가만 사용
    df["대표국가"] = (
        df["nation"]
        .fillna("알 수 없음")
        .astype(str)
        .str.split("|")
        .str[0]
    )

    # 숫자형 컬럼을 숫자로 변환
    numeric_columns = [
        "total_audi",
        "first_scrn",
        "first_week_audi"
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # 필요한 데이터가 없는 행 제거
    df = df.dropna(subset=["movieNm"])

    return df


df = load_data()


# =========================================================
# 그래프 1. 장르별 영화 편수 도넛
# =========================================================

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


# =========================================================
# 그래프 2. 장르 안의 영화 트리맵
# =========================================================

st.header("2. 장르 안의 영화 (트리맵)")

# 같은 영화가 여러 행에 존재할 수 있기 때문에
# 장르 + 영화명별로 관객수를 먼저 합칩니다.
treemap_df = (
    df.groupby(
        ["장르", "movieNm"],
        as_index=False,
        dropna=False
    )["total_audi"]
    .sum()
)

# 관객수가 없는 경우 제거
treemap_df = treemap_df.dropna(subset=["total_audi"])

fig2 = px.treemap(
    treemap_df,
    path=["장르", "movieNm"],
    values="total_audi",
    hover_data={"total_audi": ":,"}
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

st.caption("이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)")


# =========================================================
# 그래프 3. 총 관객의 분포 히스토그램
# =========================================================

st.header("3. 총 관객의 분포 (히스토그램)")

hist_df = df.dropna(subset=["total_audi"])

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

under_1m = (hist_df["tot]()
```

