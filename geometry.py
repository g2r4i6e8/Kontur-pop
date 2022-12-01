import geopandas as gpd
from shapely.geometry.polygon import Polygon
from pyproj import Transformer


def transform_coordinates(x, y, transformer):
    lon, lat = transformer.transform(y, x)
    return lon, lat


def cut_area(gpkg_file, output_file, top, left, bottom, right):
    transformer = Transformer.from_crs('EPSG:4326',
                                       'EPSG:3857')

    left, top = transform_coordinates(left, top, transformer)
    right, bottom = transform_coordinates(right, bottom, transformer)

    bounds = Polygon([(left, top),
                      (left, bottom),
                      (right, bottom),
                      (right, top),
                      (left, top)])
    gdf = gpd.read_file(gpkg_file, bbox=bounds)
    if len(gdf) < 1:
        print("Total population is 0. Probably, coordinates are not in WGS84")
        raise Exception()
    gdf['centroid'] = gdf['geometry'].centroid
    gdf = gdf[['centroid', 'population']]
    gdf['population'] = gdf['population'].astype(int)
    gdf = gdf.set_geometry('centroid')
    gdf.to_crs(crs='EPSG:4326', inplace=True)
    gdf.to_file(output_file, driver='GeoJSON', index=False, encoding='utf-8')

    population = gdf['population'].sum()
    print('Total population inside area: {}'.format(population))
    print('Output file location: {}'.format(output_file))
