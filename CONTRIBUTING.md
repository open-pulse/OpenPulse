# How to contribute to OpenPulse

We coordinate our work using GitHub, where you can find lists of [open issues](https://github.com/open-pulse/OpenPulse/issues) and [new feature requests](https://github.com/open-pulse/OpenPulse/issues?q=is%3Aissue%20state%3Aopen%20label%3A%22Feature%20request%20%3Apray%3A%22).

- [Download the repository](#download-the-repository)
- [Running from source](#running-from-source)
- [Tests](#tests)
- [Creating executables](#creating-executables)
- [Recomendations](#recomendations)

# Download the repository
This repositorty can be cloned running the following command in your terminal:
```
git clone https://github.com/open-pulse/OpenPulse.git
```

# Running from source

## Poetry
The dependencies and environments in this project are managed mainly using Poetry.
If you do not have poetry installed, you can install it running:
```
pip install poetry
```

To download and install all dependencies in a local environment run:
```
poetry install
```
This command is also usefull to reinstall the packages if some dependency changed.

When the dependencies are installed in a local virtual environment poetry can run commands
inside this environment as follows: 
```
poetry run <you command here>
```
For example, to run VIBRA the following command is required:
```
poetry run python -m vibra
```
For more information check out [poetry documentation](https://python-poetry.org/docs/).


## Conda forge
Conda is being evaluated as a tool to manage environments, specially because of packages 
only available through repositories such as conda forge.

Download and install [conda-forge](https://conda-forge.org/download/).
It is recommended to check the option *Add Miniforge3 to my PATH environment variable* in the program installation setup.
Once conda-forge was installed, it is possible to enable the MUMPS solver in Vibra. To enable this solver we need to use conda instead of poetry.
To generate the conda environment, just run:
```
conda env create -f environment.yml
```

If you are using Windows, the following commands will only work on `cmd`, and not on `powershell`.
To make this work propperly on powershell too, you need to run
```
conda init powershell
```
And then restart the `powershell` window.

After environment generation, we can activate and run Vibra by running the following commands:
```
conda activate VIBRA
```

Finally, enter the following command to execute the application:
```
python -m vibra
```

If some package changed since the generation, the environment can be updated using the following command: 
```
conda env update --f environment.yml --prune
```

# Tests
Automated tests are a great way to check if the code is running as intended, pytest is used to manage tests.
The files for automated test are placed on the folder `tests/general`.
Broader tests, that depend on the interpretation of the developer, are located in `tests/advanced/`.

To run automated tests execute: 
```
poetry run pytest
```
For more information check out [pytest documentation](https://docs.pytest.org/en/stable/).

# Interface compilation
The interfaces depend on `.ui` files that are created using Qt Designer.
Qt Designer is a tool that is installed with PySide6, and can be started with: 
```
poetry run pyside6-designer
```

After the `.ui` files are created they are compiled to `*_UI.py` files containing the classes 
that represent each QWidget. These classes can be then specialized inside the software.

The compilation process is executed with: 
```
poetry run invoke ui-compile
```


# Creating executables

## Linux
Pyinstaller is used to create executables.
In linux run the following command to create a folder containing 
a executable and its dependencies.
```
poetry run pyinstaller vibra.spec --no-confirm
```

## Windows
On windows we additionally use InnoSetup to bundle the executable folder
into a single executable installer.
InnoSetup can be installed with winget with the following command
```
winget install -e --id JRSoftware.InnoSetup
```
You may also need to add it to your Windows path.

Given that InnoSetup is correctly installed and set to path, 
to create a installer in windows run:
```
poetry run pyinstaller vibra.spec --noconfirm
ISCC.exe /O"dist" /F"vibra-setup" "vibra.iss"
```
This process might take a while, but in the end your installer will appear inside the `dist` folder, named as `open-pulse-setup-x64`.


# Recomendations

Do not use the `gif` format on README.md. Instead use `webp`, which is a file format created by google with better quality and rates of compression.

To ensure consistency, use colors from [this palette](https://andrefpf.github.io/molde/). They are easily available in the molde package, as shown in the following code snipet:
```python
from molde.colors import color_names

example_colors = [
    colornames.RED,
    GREEN_6,
    PURPLE_2,
    PURPLE_9,
    PINK_4,
]
```

A lot of free to use icons, from Material Design, are available [here](https://fonts.google.com/icons).
Other icons may be necessary, and they will be made to match the same style.
For consistency avoid using icons from other origins.
