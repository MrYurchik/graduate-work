import json
import random

# import pandas as pd
# from folium import folium
# from folium.plugins import Choropleth, LayerControl
import datetime
from flask import Flask
import folium
from folium.plugins import LocateControl
from folium import plugins

app = Flask(__name__)
f = folium.Figure(width="100%", height="100%")
m = folium.Map(location=(49.8355433005462, 24.014393882782368), zoom_start=17).add_to(f)
color_list = ['beige', 'lightblue', 'darkred', 'lightred', 'black', 'darkblue', 'darkgreen', 'orange', 'lightgray',
              'lightgreen', 'green', 'darkpurple', 'purple', 'white', 'cadetblue', 'gray', 'blue', 'pink', 'red']

now = datetime.datetime.now()

schedule_time = {1: "8:30−10:05",
                 2: "10:20−11:55",
                 3: "12:10−13:45",
                 4: "14:15−15:50",
                 5: "16:00−17:35",
                 6: "17:40−19:15",
                 7: "19:20−20:55",
                 8: "21:00−22:35"}


def time_parse():
    end = ""
    for i in schedule_time:
        start = schedule_time[i].split('−')[0]
        start = now.replace(hour=int(start.split(':')[0]), minute=int(start.split(':')[1]), second=0, microsecond=0)
        if end:
            if now < start and now > end:
                print(f"Зараз перерва, наступна пара {i}")
                break
        end = schedule_time[i].split('−')[1]
        end = now.replace(hour=int(end.split(':')[0]), minute=int(end.split(':')[1]), second=0, microsecond=0)
        if now > start and now < end:
            print(f"ЗАРАЗ {i} пара!")
            break
    return i


def get_schedule():
    with open("schedule.json", encoding="UTF-8") as file:
        today = f"{str(now.day).zfill(2)}.{str(now.month).zfill(2)}.{now.year}"
        schedule_for_today = dict()
        schedule = json.loads(file.read())
        for groups in schedule["Groups"]:
            for days in schedule["Groups"][groups]:
                if days["date"] == today:
                    print(days["date"])
                    schedule_for_today[groups] = days["lessons"]
    return schedule_for_today


def online_schedule(schedule_for_today, leson_numb):
    return {i: schedule_for_today[i][str(leson_numb)].split(':')[-1] for i in schedule_for_today}


def get_geo(schedule_for_now):
    all_geo_buildings = dict()
    with open("detail_buildings.json", encoding="UTF-8") as file:
        data = json.loads(file.read())
        for i in schedule_for_now:
            for buildings in data["features"]:
                if buildings["id"] == schedule_for_now[i]:
                    form = data.copy()
                    form["features"] = [buildings]
                    all_geo_buildings[i] = form

    return all_geo_buildings


def gen_map(build_geo):
    for groups in build_geo:
        folium.Choropleth(
            fill_color=random.choice(color_list),
            geo_data=build_geo[groups],
            name=groups,
        ).add_to(m)

    folium.LayerControl(collapsed=False).add_to(m)
    m.save("index.html")


def build_desc():
    with open("buildings.json", encoding="UTF-8") as file:
        buildings = json.loads(file.read())
    for item in buildings["all_buildings"]:
        folium.Marker(
            location=item["cord"],
            popup=f"Національний університет 'Львівська Політехніка \n Навчальний корпус №{item['numb']}' \n {item['popup']}",
            icon=folium.Icon(color=random.choice(color_list), icon="info-sign"),
        ).add_to(m)


@app.route('/')
def base():
    leson_numb = time_parse()
    schedule_for_today = get_schedule()
    schedule_for_now = online_schedule(schedule_for_today, leson_numb)
    build_geo = get_geo(schedule_for_now)
    build_desc()
    gen_map(build_geo)
    # LocateControl(enableHighAccuracy=True).add_to(m)
    # # https://github.com/domoritz/leaflet-locatecontrol#how-do-i-enable-high-accuracy
    # # ????????????????????????????????????????????
    return m._repr_html_()


if __name__ == '__main__':
    app.run(debug=True)
