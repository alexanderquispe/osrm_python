import pandas as pd, numpy as np, os
import requests

continent_df = "https://raw.githubusercontent.com/alexanderquispe/osrm_python/data/data_ref/continent_df.csv"
country_df = 'https://github.com/alexanderquispe/osrm_python/raw/data/data_ref/country_df.csv'
region_df = 'https://raw.githubusercontent.com/alexanderquispe/osrm_python/data/data_ref/region_df.csv'

cnt = pd.read_csv(continent_df)
ctry = pd.read_csv(country_df)
region = pd.read_csv(region_df)

# https://download.geofabrik.de/antarctica-latest-free.shp.zip
# https://download.geofabrik.de/asia-latest.osm.bz2
latest ='-latest'
osrm_pbf = '.osrm.pbf'
zip_ext = '-free.shp.zip'
osm_bz2 = '.osm.bz2'

def add_link_exte(where:list, ext='pbf'):

	if ext=='pbf':
		ext = osrm_pbf
	elif ext=='zip':
		ext=zip_ext
	else:
		ext=osm_bz2
	
	list_where = where.copy()
	for i, w in enumerate(where):
		list_where[i] = w + latest + ext
	return list_where


class GetPBF:
	def __init__(self, save_into_dir=None):
		print("Convert the country names to lowercase and replace spaces with dashes (-).")
		print("source: https://download.geofabrik.de/")
		if save_into_dir is None:
			save_into_dir = "data-pbf"
			if not os.path.exists(save_into_dir):
				os.makedirs(save_into_dir)
		self.dir_name = save_into_dir
	def continent(self, where:list, save_dir=None):
		if save_dir is not None:
			self.dir_name = save_dir
			if not os.path.exists(save_dir):
				os.makedirs(save_dir)
		ref=cnt.query('continent in @where').\
			url_main.to_numpy()
		ref = list(ref)
		self.locations = ref
		self.where = where
		return self
	def country(self, where:list, continent=None, save_dir=None):
		self.where = where
		if save_dir is not None:
			self.dir_name = save_dir
			if not os.path.exists(save_dir):
				os.makedirs(save_dir)
		if continent is None:
			ctrs=ctry.query('country in @where').\
				url_main.to_numpy()
			self.locations = list(ctrs)
			return self
		ctrs_spe = ctry.query('continent in @continent and country in @where').\
			url_main.to_numpy()
		self.locations = list(ctrs_spe)
		return self
	def sub_region(self, where:list, continent=None, country=None, save_dir=None):
		self.where = where
		if save_dir is not None:
			self.dir_name = save_dir
			if not os.path.exists(save_dir):
				os.makedirs(save_dir)
		if continent is None and country is None:
			sr = region.query('region in @where').url_main\
				.to_numpy()
			self.locations = list(sr)
			return self
		elif continent is not None and country is None:
			sr = region.query('continent in @continent and region in @where').\
				url_main.to_numpy()
			self.locations = list(sr)
			return self
		elif continent is None and country is not None:
			sr = region.query('country in @country and region in @where').\
				url_main.to_numpy()
			self.locations = list(sr)
			return self
		elif continent is not None and country is not None:
			sr = region.query('continent in @continent and country in @country and region in @where').\
				url_main.to_numpy()
			self.locations = list(sr)
			return self
	def get(self, ext='pbf'):
		location = self.locations
		dir_name = self.dir_name
		name_where = self.where

		download_link = add_link_exte(location, ext)
		file_name = add_link_exte(name_where)
		for i, file in enumerate(file_name):
			save_f = dir_name + '/' + file
			self._download(download_link[i], save_f)
		return self
			
	def _download(self, from_, to_):
		response = requests.get(from_)
		with open(to_, "wb") as file:
			file.write(response.content)
		





