import cx_Freeze

executables = [cx_Freeze.Executable("dodgethat.py")]

cx_Freeze.setup(
    name="A bit Racey",
    options={"build_exe": {"packages":["pygame","LeaderBoardManager","ServerManager","UserManager"],
                           "include_files":["images","fonts"]}},
    executables = executables

    )
if sys.platform == "win32":
	base = "Win32GUI"