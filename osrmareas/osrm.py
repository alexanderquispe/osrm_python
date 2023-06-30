# import areas
import os, subprocess, tempfile

# file = tempfile.NamedTemporaryFile(suffix='.bat', delete=False)
# temp_file.write(b'echo "Hello, world!"\npause')

# # Cerrar el archivo
# temp_file.close()
class Server:
	def __init__(self, pbf_file=None, pbf_file_path=None, osrm_path='C:\osrm', method_lua='car', methods_lua_path = None):

		pbf = f'{pbf_file_path}\{pbf_file}'
		osm = pbf_file.replace(".osm", "")
		osrm = f'{pbf_file_path}\{osm}.osrm'

		if methods_lua_path is None:
			lua_path = f'{osrm_path}\{method_lua}.lua'
		else:
			lua_path = f'{methods_lua_path}\{method_lua}.lua'
		
		osrm_extract = f'{osrm_path}\osrm-extract.exe'
		osrm_contract = f'{osrm_path}\osrm-contract.exe'
		osrm_routed = f'{osrm_path}\osrm-routed.exe'
		self.osrm_file = osrm
		self.pbf_file = pbf
		self._contract_file=f'{osrm}.hsgr'

		self.gen_osrm_file = f'{osrm_extract} -p {lua_path} {pbf}.pbf'
		self.gen_routes = f'{osrm_contract} {osrm}'
		self.gen_backend = f'{osrm_routed} {osrm}'

		self._prepare = False


	def gen_osrm_1(self):
		print("Please run the following function only once for each .pbf file. (It takes some time to execute, and consume all the CPU)")

		gen_osrm = self.gen_osrm_file
		osrm_file = self.osrm_file

		osrm_gen_=os.path.exists(osrm_file)

		run_first="No"

		if not osrm_gen_:
			subprocess.Popen(f'{gen_osrm}', shell=True).wait()
		else:
			print(f'Found {osrm_file} file')

			run_first = input(f"An OSRM file named '{osrm_file}' was found. Do you want to run again? [yes, no] (This will take some time)")
			if 'y' in run_first:
				subprocess.Popen(f'{gen_osrm}', shell=True).wait()
		print("Done, generate a osrm file")
		return self

	def prepare_server_2(self):
		print("Please run the following function only once for each .pbf file. (It takes some time to execute, and consume all the CPU)")

		gen_route = self.gen_routes
		contract_file = self._contract_file
		contract_ = os.path.exists(contract_file)
		run_second = "No"

		if not contract_:
			subprocess.Popen(f'{gen_route}', shell=True).wait()
		else:
			run_second = input(f"An HSGR file named '{contract_file}' was found. Do you want to run the following command again: [yes, no] (This will take some time)")
			if 'y' in run_second:
				subprocess.Popen(f'{gen_route}', shell=True).wait()
			else:
				pass
		print('Done, I have generated the local OSRM server with `{server}.run_server()`.')
		self._prepare = True
		return self

	def run_server(self):
		ready=self._prepare
		if not ready:
			raise "The necessary files are not available, please run `Server(..).gen_osrm_1()` and `Server(...).prepare_server_2()` first."

		gen_server = self.gen_backend
		

		subprocess.Popen(f'{gen_server}', shell=True)
		print("The server is running in the background, you can start making queries.")

		return self

		
		

	

		
	# def make_grid(self, x, y, size_grid):
	# 	return areas.make_grid(x, y, size_grid)
	# def get_osrm_route_local(self, from_, to_, how_='driving'):
	# 	return areas.get_osrm_route(from_, to_, how)
	# def get_area_routes(self, center, radius_km, grid_km_size=1):
	# 	routes_df = areas.get_routes(center, radius_km, grid_km_size)
	# 	self.routes_df_area = routes_df
	# 	return self
	# def get_ameba(self, df, max_km=None, alpha=0, xcol='x', ycol='y', km_col='dist_km', crs=areas.crs_lat):
	# 	ameba_shp = areas.get_ameba(df, max_km, alpha, xcol, ycol, km_col, crs)
	# 	self.ameba = ameba_shp
	# 	return self