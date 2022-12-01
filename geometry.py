import geopandas as gpd
from shapely.geometry.polygon import Polygon


def cut_area(gpkg_file, output_file, top, left, bottom, right):
    bounds = Polygon([(left, top),
                      (left, bottom),
                      (right, bottom),
                      (right, top),
                      (left, top)])
    gdf = gpd.read_file(gpkg_file, bbox=bounds)
    gdf['centroid'] = gdf['geometry'].centroid
    gdf = gdf[['centroid', 'population']]
    gdf['population'] = gdf['population'].astype(int)
    gdf = gdf.set_geometry('centroid')
    gdf.to_crs(crs='EPSG:4326', inplace=True)
    gdf.to_file(output_file, driver='GeoJSON', index=False, encoding='utf-8')

    population = gdf['population'].sum()
    print('Total population inside area: {}'.format(population))
