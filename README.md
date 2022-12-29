# EUMETSAT - Python Download

This code can be used to easily download a EUMETSAT datastore products using python.


## Anaconda Environment Setup

1) Run the following command(s) to setup the environment:
    - For Windows:
        ```
        conda env create -f environment_win.yml
        ```
    - For Linux/MacOSX:
        ```
        conda env create -f environment_unx.yml
        ```
2) To activate the environment, run:
    ```
    conda activate eumetsat
    ```
**Note:** `eumetsat` is the name of the environment. If you need to change the environment's name, edit the first line of the `environment_XXX.yml` file.


## Setting up the script to download the EUMETSAT data

In the main script to download the data, `downloadData.py`, you need to specify the following attributes:

- `consumer_key`: Your private account key obtained from the [EUMETSAT API website](https://api.eumetsat.int/api-key/).
- `consumer_secret`: Your private account secret obtained from the [EUMETSAT API website](https://api.eumetsat.int/api-key/).
- `collection_name`: The collection/product you want to download. Browse EUMETST product catalogue [here](https://data.eumetsat.int/search?query=).
- `start`: Specify the start timestamp from where onwards you wish to download the data.
- `end`: Specify the end timestamp until which you wish to download the data.
- `DATA_DIR`: Set path to the directory in which you wish to download the data.
- `pFLAG`: Boolean flag to enable or disable parallelization.
- `numDaysPerAT`: Set the number of days you wish to parse per access token. This is required to avoid Access Token timeout.

Once you have set the aforementioned attributes in the `downloadData.py` file, you can run the script from the anaconda terminal after activating the `eumetsat` environment using the following command:
```
python downloadData.py
```
**Note:** Make sure that your terminal path is same as the directory in which you have stored the `downloadData.py` file.

Upon running the script, all the available files from the EUMETSAT datastore, corresponding to the specified product name and for the specified timestamps, will be downloaded in the specified data directory. These files will be in `.zip` format and are named according to their timestamp as per the following convention:
```
yyyymmddThhMMss.zip
```
For example, a data file downloaded for `15 January 2011` and time `16:45:00`, will be saved as:
```
20110115T164500.zip
```

## License
[GNU General Public License v3.0](LICENSE)
