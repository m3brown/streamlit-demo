from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile

import altair as alt
import pandas as pd
import streamlit as st


@st.cache
def get_baseball_data():
    ZIP_URL = "https://github.com/chadwickbureau/baseballdatabank/archive/v2019.2.zip"
    with urlopen(ZIP_URL) as z:
        csv = ZipFile(BytesIO(z.read())).read(
            "baseballdatabank-2019.2/core/Salaries.csv"
        )
    df = pd.read_csv(BytesIO(csv))
    return df


st.title("Baseball Salary Trends")

df = get_baseball_data()
team_options = st.multiselect("What teams should we track?", df["teamID"].unique())
min_year = st.slider("Minimum year", min_value=1985, max_value=2016)
max_year = st.slider("Maximum year", min_value=1985, max_value=2016, value=2016)
year_range = range(min_year, max_year + 1)

df = df[df["teamID"].isin(team_options)][
    df["yearID"].isin(range(min_year, max_year + 1))
]

if team_options and year_range:
    # Create table
    st.write(
        "Salaries from {}-{} for {}".format(
            min_year, max_year, ", ".join(team_options)
        ),
        df.set_index("yearID")
        .groupby(["yearID"])
        .agg({"salary": ["sum", "min", "mean", "median"]}),
    )

    # Create graph
    c = (
        alt.Chart(df)
        .mark_circle()
        .encode(
            x=alt.X("yearID", scale=alt.Scale(domain=(min_year, max_year))),
            size="max(salary)",
            y="sum(salary)",
            color="teamID",
        )
    )
    st.altair_chart(c)
