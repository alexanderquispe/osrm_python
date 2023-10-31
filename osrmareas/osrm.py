# import areas
import os, subprocess, tempfile
import warnings

warnings.filterwarnings("ignore")

# file = tempfile.NamedTemporaryFile(suffix='.bat', delete=False)
# temp_file.write(b'echo "Hello, world!"\npause')


# # Cerrar el archivo
# temp_file.close()
class Server:
    def __init__(
        self,
        pbf_file=None,
        pbf_file_path=None,
        osrm_path="C:\osrm",
        method_lua="car",
        methods_lua_path=None,
    ):
        pbf = f"{pbf_file_path}\{pbf_file}"
        osm = pbf_file.replace(".osm", "")
        osrm = f"{pbf_file_path}\{osm}.osrm"

        if methods_lua_path is None:
            lua_path = f"{osrm_path}\{method_lua}.lua"
        else:
            lua_path = f"{methods_lua_path}\{method_lua}.lua"

        osrm_extract = f"{osrm_path}\osrm-extract.exe"
        osrm_contract = f"{osrm_path}\osrm-contract.exe"
        osrm_routed = f"{osrm_path}\osrm-routed.exe"
        self.osrm_file = osrm
        self.pbf_file = pbf
        self._contract_file = f"{osrm}.hsgr"

        self.gen_osrm_file = f"{osrm_extract} -p {lua_path} {pbf}.pbf"
        self.gen_routes = f"{osrm_contract} {osrm}"
        self.gen_backend = f"{osrm_routed} {osrm}"

        self._prepare = False

    def gen_osrm_1(self, force=False):
        gen_osrm = self.gen_osrm_file
        osrm_file = self.osrm_file

        osrm_gen_ = os.path.exists(osrm_file)

        if not osrm_gen_:
            subprocess.Popen(f"{gen_osrm}", shell=True).wait()
        else:
            print(f"Found {osrm_file} file. You can force with `force=True`")
            if force:
                subprocess.Popen(f"{gen_osrm}", shell=True).wait()
        return self

    def prepare_server_2(self, force=False):
        gen_route = self.gen_routes
        contract_file = self._contract_file
        contract_ = os.path.exists(contract_file)

        if not contract_:
            subprocess.Popen(f"{gen_route}", shell=True).wait()
        else:
            print(
                f"An HSGR file named '{contract_file}' was found. You can force with `force=True`"
            )
            if force:
                subprocess.Popen(f"{gen_route}", shell=True).wait()
            else:
                pass
        print(
            "Done, I have generated the local OSRM server with `{server}.run_server()`."
        )
        self._prepare = True
        return self

    def run_server(self):
        ready = self._prepare
        if not ready:
            raise "The necessary files are not available, please run `Server(..).gen_osrm_1()` and `Server(...).prepare_server_2()` first."

        gen_server = self.gen_backend
        subprocess.Popen(f"{gen_server}", shell=True)
        print("The server is running in the background, you can start making queries.")

        return self
