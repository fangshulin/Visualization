import altair as alt
import pandas as pd
import json

def loadData():
    import os
    cur_dir = os.path.dirname(__file__)
    restaurants = json.load(open(os.path.join(cur_dir, 'nyc_restaurants_by_cuisine.json'), 'r'))

    df_restaurant = pd.DataFrame(((d['cuisine'], number, zipcode)
                      for d in restaurants
                      for zipcode, number in d['perZip'].items()),columns=['name', 'num', 'zipcode'])
    return df_restaurant


def createChart(data, zipcode):
    color_expression    = "highlight._vgsid_==datum._vgsid_"
    color_condition     = alt.ConditionalPredicateValueDef(color_expression, "SteelBlue")
    highlight_selection = alt.selection_single(name="highlight", empty="all", on="mouseover")
    data = data[data['zipcode']==zipcode].nlargest(20, 'num')
    try:
        maxCount = int(data['num'].max())
    except ValueError:
        maxCount = 10
        data = pd.DataFrame([{"name":"no this zipcode", "num":0}])

    Number = alt.Chart(data)\
              .mark_bar(stroke="Black")\
              .encode(
                  alt.X("num:Q", axis=alt.Axis(title="Restaurants"),
                    scale=alt.Scale(domain=(0,maxCount))),
                  alt.Y('name:O', axis=alt.Axis(title="cuisine"),
                    sort=alt.SortField(field="num", op="argmax")),
                  alt.ColorValue("LightGrey", condition=color_condition),
              ).properties(
                selection = highlight_selection,
              )

    return alt.hconcat(Number,
        data=data,
    )

