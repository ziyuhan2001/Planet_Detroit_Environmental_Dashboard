import geopandas as gpd
import xml.etree.ElementTree as ET
from shapely.geometry import Point, Polygon
import pandas as pd

#Define the file paths of the KML files.
filepath1 = "filepath for KML file 1"
filepath2 = "filepath for KML file 2"
filepath3 = "filepath for KML file 3"
filepath4 = "filepath for KML file 4"
filepath5 = "filepath for KML file 5"
filepath6 = "filepath for KML file 6"
filepath7 = "filepath for KML file 7"
filepath8 = "filepath for KML file 8"

file_paths = [
    filepath1,
    filepath2,
    filepath3,
    filepath4,
    filepath5,
    filepath6,
    filepath7,
    filepath8
]

#Namespace Handling
ns = {'kml': 'http://www.opengis.net/kml/2.2'}

#Swap the positions of the blue and red level to fulfill the color format of (A,R,G,B).
def convert_color_format(color_code):
    a = color_code[:2]  # Alpha (opacity level)
    b = color_code[2:4]  # Blue level
    g = color_code[4:6]  # Green level
    r = color_code[6:8]  # Red level
    
    converted_color_code = f"{a}{r}{g}{b}"
    return converted_color_code

#Determine the climate shift index based on the color of the polygon.
def determine_climate_shift_index(color_text):
    csi_value = {
        "8C4A712A": "unavailable",
        "FF3E4143": -5,
        "FF525455": -4,
        "FF6C6D6E": -3,
        "FFACAFB1": -2,
        "FFD2D2D3": -1,
        "FFFFFFFF": 0,
        "FFF5CE5A": 1,
        "FFEC803D": 2,
        "FFE03326": 3,
        "FF9B2115": 4,
        "FF6A110A": 5,
    }
    
    return csi_value.get(color_text, "N/A")

#Create the GeoDataFrames of all the KML Files
def process_file(file_path):
    #Parse KML string
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    #Determine the color code and climate shift index of each corresponding style id
    style_info = {}
    for style in root.findall(".//Style", ns):
        style_id = style.attrib['id']
        poly_style = style.find(".//PolyStyle/color", ns)
        if poly_style is not None:
            color = convert_color_format(poly_style.text)
            climate_shift_index = determine_climate_shift_index(color)
            style_info[f"#{style_id}"] = {"Color": color, "Climate Shift Index": climate_shift_index}
    
    #Extracts information from each KML file and appends the polygon's name (ID), geometric coordinates, color ID, color, and climate shift index to the map_data list.
    map_data = []
    for placemark in root.findall(".//Placemark", ns):
        polygon_name = placemark.find(".//name", ns).text
        style_id = placemark.find(".//styleUrl", ns).text
        polygon_color = style_info.get(style_id, "N/A")["Color"]
        polygon_csi = style_info.get(style_id, "N/A")["Climate Shift Index"]
        polygon = placemark.find(".//Polygon//coordinates", ns)
        if polygon is not None:
            polygon_coordinates = polygon.text.strip().split()
            polygon_creation = Polygon([(float(lon), float(lat)) for lon, lat, _ in (coordinates.split(',') for coordinates in polygon_coordinates)])
            map_data.append({"Polygon ID": polygon_name, "Polygon Geometry": polygon_creation, "Style Color ID": style_id, "Polygon Color": polygon_color, "Climate Shift Index": polygon_csi})
        
    return gpd.GeoDataFrame(map_data, geometry="Polygon Geometry")

#Each element in climate_maps contains the extracted information from each KML file.
climate_maps = [process_file(file_path) for file_path in file_paths]

#Michigan cities and their corresponding latitude, longitude coordinates.
cities = [
    {'city': 'Benton Harbor', 'coordinates': {'lat': 42.1167, 'lon': -86.4542}},
    {'city': 'South Haven', 'coordinates': {'lat': 42.4036, 'lon': -86.2733}},
    {'city': 'Kalamazoo', 'coordinates': {'lat': 42.2917, 'lon': -85.5872}},
    {'city': 'Saugatuck', 'coordinates': {'lat': 42.6556, 'lon': -86.2014}},
    {'city': 'Lansing', 'coordinates': {'lat': 42.7325, 'lon': -84.5555}},
    {'city': 'Battle Creek', 'coordinates': {'lat': 42.3211, 'lon': -85.1797}},
    {'city': 'Grand Haven', 'coordinates': {'lat': 43.0631, 'lon': -86.2284}},
    {'city': 'Holland', 'coordinates': {'lat': 42.7875, 'lon': -86.1089}},
    {'city': 'Detroit', 'coordinates': {'lat': 42.3314, 'lon': -83.0458}},
    {'city': 'St. Clair Shores', 'coordinates': {'lat': 42.4974, 'lon': -82.8964}},
    {'city': 'Southfield', 'coordinates': {'lat': 42.4734, 'lon': -83.2219}},
    {'city': 'Southgate', 'coordinates': {'lat': 42.2133, 'lon': -83.2084}},
    {'city': 'South Lyon', 'coordinates': {'lat': 42.4614, 'lon': -83.6509}},
    {'city': 'Swartz Creek', 'coordinates': {'lat': 42.9573, 'lon': -83.8303}},
    {'city': 'Scottville', 'coordinates': {'lat': 43.9553, 'lon': -86.2740}},
    {'city': 'Ann Arbor', 'coordinates': {'lat': 42.2808, 'lon': -83.7430}},
    {'city': 'Sturgis', 'coordinates': {'lat': 41.7992, 'lon': -85.4192}},
    {'city': 'Sebewaing', 'coordinates': {'lat': 43.7325, 'lon': -83.4301}},
    {'city': 'St. Ignace', 'coordinates': {'lat': 45.8683, 'lon': -84.7225}},
    {'city': 'Springport', 'coordinates': {'lat': 42.3828, 'lon': -84.7430}},
    {'city': 'Sunfield', 'coordinates': {'lat': 42.7686, 'lon': -84.9814}},
    {'city': 'Suttons Bay', 'coordinates': {'lat': 44.9754, 'lon': -85.6483}},
    {'city': 'Sandusky', 'coordinates': {'lat': 43.4094, 'lon': -82.8234}},
    {'city': 'Traverse City', 'coordinates': {'lat': 44.7631, 'lon': -85.6206}},
    {'city': 'Hamtramck', 'coordinates': {'lat': 42.3926, 'lon': -83.0496}},
    {'city': 'Berkley', 'coordinates': {'lat': 42.5031, 'lon': -83.1837}},
    {'city': 'Highland Park', 'coordinates': {'lat': 42.3926, 'lon': -83.0890}},
    {'city': 'Dearborn Heights', 'coordinates': {'lat': 42.3361, 'lon': -83.2733}},
    {'city': 'Farmington', 'coordinates': {'lat': 42.4645, 'lon': -83.3763}},
    {'city': 'Ecorse', 'coordinates': {'lat': 42.2446, 'lon': -83.1392}},
    {'city': 'Saint Charles', 'coordinates': {'lat': 43.2861, 'lon': -84.1236}},
    {'city': 'East Lansing', 'coordinates': {'lat': 42.7360, 'lon': -84.4839}},
    {'city': 'Ypsilanti', 'coordinates': {'lat': 42.2411, 'lon': -83.6129}},
    {'city': 'Rockford', 'coordinates': {'lat': 43.1200, 'lon': -85.5600}},
    {'city': 'Dearborn', 'coordinates': {'lat': 42.3223, 'lon': -83.1763}},
    {'city': 'Novi', 'coordinates': {'lat': 42.4801, 'lon': -83.4755}},
    {'city': 'Sterling Heights', 'coordinates': {'lat': 42.5803, 'lon': -83.0302}},
    {'city': 'Farmington Hills', 'coordinates': {'lat': 42.4982, 'lon': -83.3677}},
    {'city': 'Auburn Hills', 'coordinates': {'lat': 42.6875, 'lon': -83.2341}},
    {'city': 'Wyandotte', 'coordinates': {'lat': 42.2042, 'lon': -83.1499}},
    {'city': 'Alpena', 'coordinates': {'lat': 45.0617, 'lon': -83.4327}},
    {'city': 'Coldwater', 'coordinates': {'lat': 41.9403, 'lon': -85.0006}},
    {'city': 'Port Huron', 'coordinates': {'lat': 42.9826, 'lon': -82.4387}}
]

#Convert latitude and longitude coordinates into a point geometry.
cities_data = gpd.GeoDataFrame(cities)
cities_data["Point Geometry"] = cities_data.apply(lambda x: Point(x["coordinates"]["lon"], x["coordinates"]["lat"]), axis=1)
cities_data = cities_data.set_geometry("Point Geometry")
cities_data = cities_data.drop(columns=["coordinates"])

#Determine whether a city is in a Polygon or not. If so, determine which polygon and the corresponding characteristics.
def city_in_polygons(cities_gdf, polygons_gdf):
    city_polygons = []
    
    for city_index, city_row in cities_data.iterrows():
        city_name = city_row["city"]
        city_point = city_row["Point Geometry"]
        
        # Check if the city point in any polygon (in or on the boundary of)
        in_polygon = polygons_gdf[polygons_gdf.intersects(city_point)]
        
        if not in_polygon.empty:
            for polygon_index, polygon_row in in_polygon.iterrows():
                city_polygons.append({"city": city_name, "Point Geometry": city_point, "Polygon ID": polygon_row["Polygon ID"], "Associated Polygon": polygon_row["Polygon Geometry"], "Polygon Color ID": polygon_row["Style Color ID"], "Polygon Color": polygon_row["Polygon Color"], "CSI": polygon_row["Climate Shift Index"]})
        else:
            city_polygons.append({"city": city_name, "Point Geometry": city_point, "Polygon ID": "undetectable", "Associated Polygon": "undetectable", "Polygon Color ID": "undetectable", "Polygon Color": "undetectable", "CSI": "undetectable"})
    
    cities_csi = gpd.GeoDataFrame(city_polygons)
    cities_csi = cities_csi.drop(columns=["Polygon ID", "Associated Polygon", "Polygon Color ID", "Polygon Color"])
    cities_csi["CSI"] = pd.to_numeric(cities_csi["CSI"], errors="coerce")

    cities_csi = cities_csi.groupby("city", as_index=False).agg({
        "Point Geometry": "first",
        "CSI": "mean"
    })
    
    cities_csi["CSI"] = cities_csi["CSI"].astype(str)
    cities_csi["CSI"] = cities_csi["CSI"].replace("nan", "undetectable")
    
    return cities_csi

#Obtaining the CSI information for tmin and tmax (yesterday, today, tomorrow, day after tomorrow) under each city.
result_tmin_yesterday = city_in_polygons(cities_data, climate_maps[0])
result_tmin_today = city_in_polygons(cities_data, climate_maps[1])
result_tmin_tomorrow = city_in_polygons(cities_data, climate_maps[2])
result_tmin_day_after_tomorrow = city_in_polygons(cities_data, climate_maps[3])

result_tmax_yesterday = city_in_polygons(cities_data, climate_maps[4])
result_tmax_today = city_in_polygons(cities_data, climate_maps[5])
result_tmax_tomorrow = city_in_polygons(cities_data, climate_maps[6])
result_tmax_day_after_tomorrow = city_in_polygons(cities_data, climate_maps[7])

#Changing the name of the CSI column to distinguish between datasets.
result_tmin_yesterday.rename(columns={"CSI": "CSI (Yesterday)"}, inplace=True)
result_tmin_today.rename(columns={"CSI": "CSI (Today)"}, inplace=True)
result_tmin_tomorrow.rename(columns={"CSI": "CSI (Tomorrow)"}, inplace=True)
result_tmin_day_after_tomorrow.rename(columns={"CSI": "CSI (Day After Tomorrow)"}, inplace=True)

result_tmax_yesterday.rename(columns={"CSI": "CSI (Yesterday)"}, inplace=True)
result_tmax_today.rename(columns={"CSI": "CSI (Today)"}, inplace=True)
result_tmax_tomorrow.rename(columns={"CSI": "CSI (Tomorrow)"}, inplace=True)
result_tmax_day_after_tomorrow.rename(columns={"CSI": "CSI (Day After Tomorrow)"}, inplace=True)

#Merging tmin data information under one dataset and tmax data information under one dataset.
tmin_data = pd.merge(result_tmin_yesterday, result_tmin_today, on=["city", "Point Geometry"], how="outer")
tmin_data = pd.merge(tmin_data, result_tmin_tomorrow, on=["city", "Point Geometry"], how="outer")
tmin_data = pd.merge(tmin_data, result_tmin_day_after_tomorrow, on=["city", "Point Geometry"], how="outer")

tmax_data = pd.merge(result_tmax_yesterday, result_tmax_today, on=["city", "Point Geometry"], how="outer")
tmax_data = pd.merge(tmax_data, result_tmax_tomorrow, on=["city", "Point Geometry"], how="outer")
tmax_data = pd.merge(tmax_data, result_tmax_day_after_tomorrow, on=["city", "Point Geometry"], how="outer")

#Convert datasets into geodataframes.
tmin_data = gpd.GeoDataFrame(tmin_data, geometry="Point Geometry")
tmax_data = gpd.GeoDataFrame(tmax_data, geometry="Point Geometry")

#Convert Point Geometry back into separate latitude and longitude columns for analysis.
tmin_data["Latitude"] = tmin_data["Point Geometry"].y
tmin_data["Longitude"] = tmin_data["Point Geometry"].x
tmin_data = tmin_data.drop(columns=["Point Geometry"])

tmax_data["Latitude"] = tmax_data["Point Geometry"].y
tmax_data["Longitude"] = tmax_data["Point Geometry"].x
tmax_data = tmax_data.drop(columns=["Point Geometry"])

#Change the order of columns for convenience.
tmin_data = tmin_data[["city", "Latitude", "Longitude", "CSI (Yesterday)", "CSI (Today)", "CSI (Tomorrow)", "CSI (Day After Tomorrow)"]]
tmax_data = tmax_data[["city", "Latitude", "Longitude", "CSI (Yesterday)", "CSI (Today)", "CSI (Tomorrow)", "CSI (Day After Tomorrow)"]]

#Save the minimum and maximum temperature CSI data to CSV files.
tmin_file_path = ".csv filepath for tmin file"
tmax_file_path = ".csv filepath for tmax file"

tmin_data.to_csv(tmin_file_path, index=False)
tmax_data.to_csv(tmax_file_path, index=False)