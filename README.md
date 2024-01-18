# Project information

This project intends to find a solution to the ongoing (at the time of writing January 2024) kaggle competition [SenNet + HOA - Hacking the Human Vasculature in 3D](https://www.kaggle.com/competitions/blood-vessel-segmentation/overview)

## Project description

Here's a summary of project description:

The goal of the competition is to segment blood vessels . You will create a model trained on 3D Hierarchical Phase-Contrast Tomography (HiP-CT) data from human kidneys to help complete a picture of vasculature throughout a body.

Your work will better researchers' understanding of the size, shape, branching angles, and patterning of blood vessels in human tissue.

Please see the detailed description on the [competitions' page](https://www.kaggle.com/competitions/blood-vessel-segmentation/overview/description)


# Reproduce the work

## Create environment

**Disclaimer:**  
I prefer to use conda because it comes with a Python interpreter of the specified version whereas with the other options like pipenv, poetry etc you need a base interpreter of a required version.
If you don't want to use conda, you can as well skip the conda environment setup and use the provided Pipfile.* to reproduce the environment or create a virtual environment of your choice (eg python's built-in `venv`), and install the dependencies using the provided [requirements.txt](requirements.txt). In the latter case you need to remember that the base interpreter's python version must be 3.10 and that 100% reproducibility is likely to be achieved but is not guaranteed.

Below are instructions for conda:

1. Clone this repo

1. Create a clean Python 3.10 based environment and activate it
    ```shell
    conda create -n blood-vessel-segmentation python=3.10
    conda activate blood-vessel-segmentation
    ```

1. Install requirements
    ```shell
    pip install -r requirements.txt 
    ```

## Run the notebooks

Spin up a jupyter server and use your browser to open a notebook from the [notebooks folder](notebooks/) by executing:

**Note on Windows OS**:  
There is some bash script used in the notebooks. I'm not 100% sure it will execute properly on **Windows** within the notebook. If it doesn't just follow the existing notebooks output.


```shell
jupyter notebook
```

Notebooks description:


