# Contribution Guide

## Setting up the project

Clone the project into your machine 
```sh
git clone https://github.com/prakash-O4/magiccommits.git
```

Activate virtual environment
```sh
python3 -m venv .venv
```

Activate virtual environment
```sh
source .venv/bin/activate
```

Install the dependencies using pip:
```sh
pip3 install -r requirements.txt
```


### Development mode
During development, to automatically rebuild the package on file changes:
```sh
pip3 install -e .
```

## Running the package locally
If you want to run the package outside of venv then you can build the executable file which will be stored inside the **dist/** folder
```sh
python3 -m build --sdist
```

After building the execcutable, now you can install the file by executing
```sh
pip3 install /path/to/dist/***.gz
```

This will install the magiccommits in your machine locally and you can execute globally.

If you faced any issue then feel free to open PR in https://github.com/prakash-O4/magiccommits/issues.
