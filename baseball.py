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
options = st.multiselect("What teams should we track?", df["teamID"].unique())
df = df[df["teamID"].isin(options)]

if options:
    # Create table
    st.write(
        "Salaries",
        df.set_index("yearID")
        .groupby(["yearID"])
        .agg({"salary": ["sum", "min", "mean", "median"]}),
    )

    # Create graph
    c = (
        alt.Chart(df)
        .mark_circle()
        .encode(
            x=alt.X("yearID", scale=alt.Scale(domain=(1985, 2016))),
            size="max(salary)",
            y="sum(salary)",
            color="teamID",
        )
    )
    st.altair_chart(c)
