T411 CLI
===================

[![PyPi](https://img.shields.io/pypi/v/t411cli.svg)](https://pypi.python.org/pypi/t411cli)


**t411cli** is a lightweight command line interface / API for T411 written in Python.

[![Interface](https://github.com/Xide/t411cli/blob/master/screenshot.png)]


----------
Installation
-------------

### Via pip

```sh
pip3 install t411cli
```

### The basic way

```sh
git clone git@github.com:Xide/t411cli.git
cd t411cli/
pip3 install -r requirements.txt
python3 ./setup.py install
```
Use this method if you want the lastest (maybe less stable) updates.


> Note: The code is not yet compatible with python2

----------
Quick Start
-------------

At first run, the soft will ask for your T411 credentials, simply type them once and they will be stored under ``` /home/$USER/.config/t411cli.conf ``` (See [Configuration](#configuration) section for more details.)
> Note: You can override configuration path with **-c** | **--configuration** command line option

**t411cli** main commands:

> **search**
> Command used to browse available torrents.

> **details**
> Get details for a specific torrent.

> **download**
> Download selected torrent to filesystem.

> **top**
> Retreive top torrents

> **bookmark**
> Bookmarks management

If you want more details about a command usage, you can use the following help pages:
```sh
t411 command -h
```

#### Search for a torrent

You can browse T411 by by simply typing:
```sh
t411 search 'torrent name'
```
The 10 best matches (ordered by number of seeders) will be shown, if you want to change this number, you can just set the ``` --limit | -l ``` argument like so:

```sh
t411 -l 50      search 'torrent name' # OR
t411 --limit 50 search 'torrent name' # Both command will give the same results
```
Or you can just browse in the most popular torrents:
```sh
t411 top [100|day|week|month]
```
##### Sort torrents
The search and top features handle sorting options:
```sh
t411 search "query" seed desc # Sort result by number of seeders (default behaviour)
t411 top day size asc # Less heavy torrents of the day
```
search options are:
> size
> seed
> leech
> download

You can order sorting  with **asc** or **desc** specifier.

Those  commands will yield a list of torrents, To use the other commands, please be sure to **note the torrent ID** displayed.

#### Download a torrent

In order to download a torrent, you must have his ID;
```sh
t411 download TORRENT_ID
```

You can specify a command to launch on download completion, for example:

```sh
t411 download TORRENT_ID --cmd 'qbittorrent %torrent'
```
Will open the corresponding torrent in qbittorrent.

> **Note**
> The special keyword **%torrent** can be used in **--cmd** option to refer to the completed torrent file.

By default, your torrent file will be stored under ```/home/$USER/Downloads``` directory, see [Configuration](#Configuration) section to change this behaviour.


#### Manage bookmarks

You can use your t411 bookmarks directly from the command line using the  ```t411 bookmark``` command.

this command will yield a list of all your bookmarked torrents, you can add or delete existing bookmarks with the ```t411 bookmark add TORRENT_ID``` and ```t411 bookmark del TORRENT_ID``` subcommands.

----------
Configuration
-------------

By default, your configuration will be loaded or stored from:
``` /home/$USER/.config/t411cli.conf ```
You can also put a global configuration in the ```/etc/t411cli.conf``` file

The tool configuration is split in two parts:

**Account**
> Section containing account information : username and password

> Warning: T411 credentials will be stored on your file system unencrypted, you might want to use **-p** command line argument instead if you are using this soft on a public computer.

**Config**
> Section for software configuration

* limit
   > Maximum number of torrent that can be fetched in a single request

* torrent_folder
	> The tool will download torrent files in this folder

----------
Troubleshooting
-------------

Getting a ```ServiceError``` on program startup:
> This error is usually used when T411 is unreachable or encounter an unknown problem, check for [API status](http://www.websitedown.info/api.t411.in)
> If this service is up, please contact a project developer

----------
Developers
-------------

Hi, wanna join us ? Glad to hear that !
You can start browse the code, we are trying to comment a lot, especially for TODO's.
Or you can try to improve one of theses :

	- Test coverage
	- Command line utilities
	- Windows compatibility
	- Fancy colors and stuff


