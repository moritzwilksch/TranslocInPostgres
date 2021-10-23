#%%
import requests
import pandas as pd
import plotly.express as px


#%%

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:94.0) Gecko/20100101 Firefox/94.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.5",
    "Origin": "https://triangle.transloc.com",
    "Connection": "keep-alive",
    "Referer": "https://triangle.transloc.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
}

params = (
    ("agencies", "20,8,176,24,16,12,367,575,683,1749"),
    ("include_arrivals", "true"),
)


def fetch_data():
    # request data from Transloc
    response = requests.get(
        "https://feeds.transloc.com/3/vehicle_statuses", headers=headers, params=params
    )

    r = response.json()

    # only use subset and build dataframe
    use_cols = ["id", "route_id", "position", "heading", "speed"]
    df = pd.DataFrame(r["vehicles"])[use_cols]
    df = df.assign(
        lat=df.position.apply(lambda x: x[0]), lng=df.position.apply(lambda x: x[1]),
    )

    # return dataframe and raw json response
    return df, r




#%%

if __name__ == "__main__":
    df, _ = fetch_data()

    fig = px.scatter_mapbox(
        df,
        lat="lat",
        lon="lng",
        hover_data=["id", "route_id", "speed"],
        color_discrete_sequence=["fuchsia"],
        zoom=10,
        height=600,
        size="speed",
        size_max=15,
    )
    fig.update_layout(mapbox_style="open-street-map")

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.show()
