# Golem Run Script - simple tool to execute any script on Golem network

This PoC demonstrates a potential tool for Golem Network creators and requestors - `golem-run`. This utility allows to 
execute simple scripts on Golem network without a need to understand Golem internals nor JS/Python Yagna API's. 

## Demo

![demo](https://user-images.githubusercontent.com/5244214/184361089-c1b33ef8-4df2-4723-975e-6f54a855b6fb.gif)

## Installation

Tool is adjusted to be installable from PyPI already, but since it's not yet released, the only way to use this tool is
to download the source code and install package manually. To do so, follow steps below

```
$ git clone https://github.com/VanDavv/golem-run.git
$ cd golem-run
$ python3 setup.py install
```

These two lines should install the package and allow you to use `golem-run` command. In case there are any issues with
the setup, feel free to [create an issue]()

## Usage

Run script on Golem network (no arguments)

```
$ golem-run examples/test_hello.js 
```

If you'd like to provide arguments, you can provide one...

```
$ golem-run examples/test_hello.py Łukasz
```

Or multiple...

```
$ golem-run examples/test_collatz.js 20 30
```

There are also two additional arguments that can be passed to change the runtime behavior:

- `-img / --image` flag that allows to specify Docker tag name to be used for script execution
- `-exe / --executable` flag that allows to specify path inside the Docker container that will execute the script

If you're using Python (`.py`) or JavaScript (`.js`) scripts and omit those flags, this tool will load the defaults
corresponding to the script type to be able to execute it.

Full help output

```
$ golem-run --help
usage: golem-run [-h] [-exe EXECUTABLE] [-img IMAGE] file [params ...]

positional arguments:
  file                  Specify script path
  params                Specify script arguments

optional arguments:
  -h, --help            show this help message and exit
  -exe EXECUTABLE, --executable EXECUTABLE
                        Specify path inside runtime container to script executable
  -img IMAGE, --image IMAGE
                        Specify path inside runtime container to script executable
```