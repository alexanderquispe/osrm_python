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


	def prepare_server(self):
		if self._prepare:
			return "Done!"
		print("Please run the following function only once for each .pbf file. (It takes some time to execute, and consume all the CPU)")
		gen_osrm = self.gen_osrm_file
		gen_route = self.gen_routes
		osrm_file = self.osrm_file
		pbf_file = self.pbf_file
		comand = f'''
{gen_osrm}
{gen_route}
			'''
		comand1 = comand
		
		run_first = 'no'
		run_second = 'no'

		fl = tempfile.NamedTemporaryFile(delete=False, suffix='.bat')
		file = fl.name

		if os.path.exists(osrm_file):
			print('Found osrm file')
			run_first = input(f"An OSRM file named '{osrm_file}' was found. Do you want to run the following command again: `osrm_extract.exe -p car.lua {pbf_file}`? [yes, no] (This will take some time)")
		else:
			with open(file, 'w') as bt:
				bt.write(comand1)
			subprocess.Popen(['start', 'cmd', '/c', 'call', file], shell = True)
			print(file)
			print(comand1)
		
		if "n" in run_first:
			comand = f'''
{gen_route}
			'''

		if os.path.exists(self._contract_file):
			print('Found contract file')
			run_second=input(f"Contract found, run again?")
		
		if 'n' in run_second:
			comand = ''
		with open(file, 'w') as bt:
			bt.write(comand)
		subprocess.Popen(['start', 'cmd', '/c', 'call', file], shell = True)
		self._prepare = True
		return self
	def run_server(self):
		gen_server = self.gen_backend
		comand = f'''
{gen_server}
		'''
		fl = tempfile.NamedTemporaryFile(delete=False, suffix='.bat')
		file = fl.name

		with open(file, 'w') as bt:
			bt.write(comand)
		subprocess.Popen(['start', 'cmd', '/c', 'call', file], shell = True)
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