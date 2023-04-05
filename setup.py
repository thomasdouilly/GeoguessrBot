from cx_Freeze import setup, Executable

base = None
executables = [Executable("launch.py", base=base)]

packages = ["os", "subprocess"]
options = {
    'build_exe': {    
        'packages':packages,
    },
}
setup(
    name = "GeoguessrBot",
    options = options,
    version = "0.1",
    description = 'Local server in which runs the GeoEstimation model when required by the Extension',
    executables = executables
)