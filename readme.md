# Pre requirements

## Windows

- Please download the [release archive](https://github.com/christophrust/osrmtime/releases/download/v1.3.3/osrmtime_release1.3.3.zip) and unpack it at a location of your choice.
  - Recommended:
    - Make `osrm` directory into `C:\`:
  - Uncompress the folder `osrm_win_v5.14` and `dll-x64`, and move all the files inside the `C:\osrm` folder.
  - At the end, the files inside the folder should have similar characteristics to this tree.
  ```
  |-- api-ms-win-crt-runtime-l1-1-0.dll
  |-- bicycle.lua
  |-- car.lua
  |-- debug_example.lua
  |-- examples
  |   `-- postgis.lua
  |-- foot.lua
  |-- lib
  |   |-- access.lua
  |   |-- destination.lua
  |   |-- guidance.lua
  |   |-- maxspeed.lua
  |   |-- pprint.lua
  |   |-- profile_debugger.lua
  |   |-- relations.lua
  |   |-- sequence.lua
  |   |-- set.lua
  |   |-- tags.lua
  |   |-- utils.lua
  |   `-- way_handlers.lua
  |-- libexpat.dll
  |-- lua.dll
  |-- msvcp140.dll
  |-- osrm-components.exe
  |-- osrm-contract.exe
  |-- osrm-customize.exe
  |-- osrm-datastore.exe
  |-- osrm-extract.exe
  |-- osrm-partition.exe
  |-- osrm-routed.exe
  |-- osrm.lib
  |-- osrm_contract.lib
  |-- osrm_customize.lib
  |-- osrm_extract.lib
  |-- osrm_partition.lib
  |-- osrm_store.lib
  |-- osrm_update.lib
  |-- psu_lat_long_radius.csv
  |-- rasterbot.lua
  |-- rasterbotinterp.lua
  |-- tbb.dll
  |-- tbbmalloc.dll
  |-- tbbmalloc_proxy.dll
  |-- test.lua
  |-- testbot.lua
  |-- turnbot.lua
  |-- vcomp140.dll
  |-- vcruntime140.dll
  ```
- Add `osrm` to path

  - `Edit the system enviroment variable`, `Environment Variables`, `System Variables`, `path`, `New` (`path/to/osrm/files/`), `ok` (x3)
    <!-- -  -->

    ![](figs/01-path.png)
    ![](figs/02-path.png)

# Work with `osrm` localy:

- Download a `pbf` file: [Link](https://download.geofabrik.de/)
- Move the file to your working environment.
  - Recomend -> Make a data directory `osrmdata`
- Open the terminal and change the directory to your working environment.

Done!

# Python library

## Installation

github

```
pip install git+https://github.com/alexanderquispe/osrm_python
```

## Usage

Chile Example, [dbf]()

```py
from osrmareas.osrm import  Server
from osrmareas import  areas
all = areas.get_routes([-20.2015383, -70.1575468], radius_km=20)
```

Connection

```python
pbf_file = 'chile-latest.osm'
pbf_file_path = 'D:\Workflow\work\osrm-backend\data'
client = Server(pbf_file, pbf_file_path)
client.prepare_server()
client.run_server()
```

Areas

```python
all = areas.get_routes([-20.2015383, -70.1575468], radius_km=10)
all.plot()
areas.get_ameba(all, 5, alpha = 80).plot()
```
