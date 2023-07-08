import requests, pandas as pd, alphashape
from tqdm import tqdm
import geopandas as gpd, numpy as np
from shapely.geometry import LineString, Point
from shapely.geometry import Polygon

crs_moll='EPSG:3857'
crs_lat='EPSG:4326'

def make_grid(x, y, size_grid):
	coords_pol = [
		(x, y), (x + size_grid, y), 
		(x + size_grid, y + size_grid), 
		(x, y + size_grid)]
	center = size_grid / 2
	coords_center = [x + center, y + center] 
	coords_center = Point(coords_center)
	pc = gpd.GeoSeries(coords_center, crs=crs_moll)\
		.to_crs(crs_lat)
	lat, lon = pc.x, pc.y
	destiny = list(np.array([lat, lon]).flatten())
	pc_list = pc.tolist()
	pol = Polygon(coords_pol)
	gdf = gpd.GeoDataFrame({'geometry': pol}, index=[0])\
		.set_crs(crs_moll)\
		.to_crs(crs_lat)
	return destiny#pc#gdf, pc_list, 

def get_osrm_route(from_, to_, how='driving'):
	
	url = f'http://127.0.0.1:5000/route/v1/{how}/'
	url += f'{from_[1]},{from_[0]};{to_[1]},{to_[0]}?steps=true&geometries=geojson&annotations=duration&alternatives=false'

	r = requests.get(url)
	rjson = r.json()
	crs_lat='EPSG:4326'
	crs_moll='EPSG:3857'
	info = rjson['routes'][0]
	dist = info['distance']
	route = info['geometry']['coordinates']
	# route.append([-66.744416, -54.975603])dd
	line = gpd.GeoDataFrame(geometry=[LineString(route)]).set_crs(crs_lat)
	line = line.assign(
		dist_driving_km=dist/1000, dest_lon = to_[0], dest_lat = to_[1],
		origin_lon = from_[0], origin_lat = from_[1]
	)
	return line

def get_routes(
	center_lat_long, radius_km=10, grid_km_size=1, filter_km=True
	):

	n_grid = radius_km/grid_km_size * 2
	center = list(reversed(center_lat_long))
	radius_km = radius_km * 1000
	initial_center = Point(center)

	point_center = gpd.GeoSeries(initial_center, crs=crs_lat)\
		.to_crs(crs_moll)\
			.buffer(radius_km, cap_style=3)
	minX, minY, maxX, maxY = point_center.total_bounds
	size_grid_km = (maxY - minY) / n_grid
	cols_grid=list(np.arange(minX, maxX, size_grid_km))
	rows_grid=list(np.arange(minY, maxY, size_grid_km))
	# grids centroid
	final_routes = []
	for x in cols_grid:
		for y in rows_grid:
			final = make_grid(x, y, size_grid_km)
			final_routes.append(final)
	# osrm routes
	all_routes_df = gpd.GeoDataFrame()
	for final in tqdm(final_routes):
		center1 = list(reversed(center))
		final1 = list(reversed(final))
		all_routes_df = \
			pd.concat([all_routes_df, get_osrm_route(center1, final1)])
	
	if filter_km:
		a = f'dist_driving_km <= {radius_km}'
		print(a)
		crop = all_routes_df.query(f'dist_driving_km <= {radius_km}')
		return crop
	
	return all_routes_df

def get_ameba(df, max_km=None, alpha = 0, xcol='dest_lon', ycol='dest_lat', km_col='dist_driving_km', crs=crs_lat):
	if max_km is None:
		max_km=np.mean(df[km_col])
	crop_df = df.copy()
	if km_col is not None:
		crop_df_rows = df[km_col] < max_km
		# crop_df = df.query("@km_col < @max_km")
		crop_df = df.loc[crop_df_rows]
	border = []
	for _, row in crop_df.iterrows():
		border.append((row[ycol], row[xcol]))
	bd = alphashape.alphashape(border, alpha)
	gdf = gpd.GeoDataFrame(geometry=[bd])
	if crs is not None:
		gdf=gdf.set_crs(crs, allow_override=True)
	return gdf