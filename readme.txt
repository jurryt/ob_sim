Odd.Bot simulation environment

*** Works on Ubuntu linux with: ***

- Anaconda Python 3
https://repo.continuum.io/archive/Anaconda3-5.1.0-Linux-x86_64.sh
- mongodb server
sudo apt install mongodb-server 
- ffmpeg encoder (to make movies)
sudo apt install ffmpeg
- ...

*** How to run: ***

- start Spyder IDE
spyder
- open world.py, machines.py and views.py
For all set the Run configuration per file to executed in dedicated console
- Under preferences -> IPython Console -> Graphics 
set backedn to automatic
- run world.py (do not close)
- run machines.py (do not close)
- run views.py (do not close) should show anitmated contour and mesh plot

To create a movie set MOVIE in settings.py to True and rerun views.py


*** What's next ***

- replace mongodb with bigchaindb
- implement package delivery with (iota) eJoule transactions
- implement machine behaviour
- plot per machine grid
- make blender viewer
- implement node structure (machine with energy, information and subnode structure)
- more realistic simulation, z-coordinates, collision, machine spatial orientation
- scenario loader (package delivery, satellites, teleportation,...)
- ...

 
