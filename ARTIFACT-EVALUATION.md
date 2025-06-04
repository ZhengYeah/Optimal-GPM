# Artifact Appendix

Paper title: Optimal Piecewise-based Mechanism for Collecting Bounded Numerical Data under Local Differential Privacy

Artifacts HotCRP Id: #4

Requested Badge: Available, Functional, Reproduced

## Description
This paper studies the optimality of piecewise-based mechanisms under the most general form. Our artifact includes the source code and datasets necessary to reproduce the experimental results presented in the paper.

We have simplified the reproduction process — it should take less than 20 minutes if you are familiar with Python-based projects.

### Security/Privacy Issues and Ethical Concerns (All badges)
The artifact does not require any security modifications for installation or execution. Most evaluations are theoretical or comparative in nature. The dataset included is small and publicly available, with no sensitive information involved.

## Basic Requirements (Only for Functional and Reproduced badges)
### Hardware Requirements
The code has been tested on both Windows desktops and laptops. Standard hardware with a typical CPU and 16GB of memory should be sufficient.

### Software Requirements
The artifact is implemented entirely in Python. It only requires a working Python environment. Development was done using PyCharm, and the artifact has been tested on various Windows and Linux systems.

### Estimated Time and Storage Consumption
* **Time**: Approximately 20 minutes in total, including dependency installation. Once dependencies are installed, reproducing the results takes about 10 minutes.

* **Storage**: The full installation (including dependencies) occupies approximately 350MB.

## Environment 
### Accessibility (All badges)

GitHub repository: https://github.com/ZhengYeah/Optimal-GPM/

Commits after `4c8b33f` (dated June 4) are expected to work.

### Set up the environment (Only for Functional and Reproduced badges)

**Install UV package manager.** This project is packaged by `uv`, a modern Python package management system similar to `miniconda` or `poetry`.

All dependencies are listed in `pyproject.toml`.

We recommend using `uv` to create a virtual environment and install the dependencies. To install `uv`, follow the instructions in the "[uv installation](https://docs.astral.sh/uv/)".

After installation, follow the prompts to add `uv` to your system's `PATH`. You can verify the installation by running the following command in your terminal (Windows, Linux, or macOS):

```
uv --version
```
This should display the installed version of `uv`.

**Install dependencies.** After installing `uv`, cd to the project root directory and run:

```
[PROJECT_ROOT]$ uv sync
```

This command creates a virtual environment in the project root and installs the dependencies listed in `pyproject.toml`. 

### Testing the Environment (Only for Functional and Reproduced badges)
To verify that the dependencies have been installed correctly, run the following command from the project root:
```
[PROJECT_ROOT]$ uv pip check
```

This will print: all installed packages are compatible.

## Artifact Evaluation (Only for Functional and Reproduced badges)

### Main Results and Claims
#### Main Result 1: Comparison with PM-C and SW-C
(Figure 8–11, Page 10) OGPM demonstrates smaller expected errors compared to PM-C and SW-C.

#### Main Result 2: Comparison with Original PM and SW

(Figure 12, Page 11) OGPM shows smaller expected errors than the original PM and SW mechanisms on their respective data domains.

#### Main Result 3: Comparison with Original PM and SW

(Figure 13–15, Pages 11–12) OGPM is compared with other non-piecewise-based mechanisms, showing improved performance in expected error.

#### Main Result 4: Comparison of Estimations on Real-world Datasets

(Figure 16–17, Page 12) OGPM is tested on real-world datasets, outperforming PM-C and SW-C in terms of accuracy.

You can reproduce these results using the provided scripts. Two options are available:

1. Use the main reproduction scripts in the `reproduction` folder. (Option 1)
2. Run individual scripts in the `experiments` folder. (Option 2)

### Experiments -- Option 1 (Quick) -- Recommended

The `reproduction` folder contains scripts  to reproduce key results from the paper. The structure is as follows:

```
|- reproduction
  |- figure_8_11.py: Figure 8a, 9a, 10a, 11b (Page 10)  (<1 minute)
  |- figure_12.py: Figure 12a and 12b (Page 11)  (<1 minute)
  |- figure_13_15.py: Figure 13a, 14, 15 (Page 11~12)  (<1 minute)
  |- figure_16_17.py: Figure 16a and 17a (Page 12)  (subsampled, <5 minutes)
```

You can run these scripts directly with `uv run` (no need to manually activate the environment). For example, to generate the first group of figures:

```
[PROJECT_ROOT]$ uv run ./reproduction/figure_8_11.py
```

This will display the corresponding figures using matplotlib.

Some figures are omitted due to minor parameter differences, for brevity. The last script is a subsampled version of the original one to speed up the reproduction. It may slightly differ from the original figure in the paper, but the overall trend remains the same. The fine-grained results can be obtained by running the scripts in the `experiments` folder.

#### Experiment 1: Comparison with PM-C and SW-C

To reproduce the first result, run 

```
[PROJECT_ROOT]$ uv run ./reproduction/figure_8_11.py
```

#### Experiment 2: Comparison with Original PM and SW

```
[PROJECT_ROOT]$ uv run ./reproduction/figure_12.py
```

#### Experiment 3: Comparison with Original PM and SW

```
[PROJECT_ROOT]$ uv run ./reproduction/figure_13_15.py
```

#### Experiment 4: Comparison of Estimations on Real-world Datasets

```
[PROJECT_ROOT]$ uv run ./reproduction/figure_16_17.py
```

### Experiments -- Option 2 (Detailed)

The `experiments` folder contains all scripts used in the paper, including intermediate results and full figures.
These scripts rely on PyCharm’s path configuration. To run them, you need the PyCharm GUI and run them by right-clicking the script.

The scripts are organized as follows:

```
|- experiments
  |- theoretical
    |- classical_domain
      |- whole_domain_L1.py: Figure 8
      |- worst_case_L1.py, worst-case_L2.py: Figure 9
      |- comparison_truncated_and_staircase: Figure 13 and 14
      |- small_epsilon: Figure 20 in the appendix
    |- circular_domain
      |- whole_domain_circular_L2.py: Figure 10
      |- worst_case_circular_L1.py, worst-case_circular_L2.py: Figure 11
      |- comparison_purkayastha: Figure 15
    |- ablation
      |- ablation_whole_domain_L2_PM.py: Figure 12(a)
      |- ablation_whole_domain_L2_SW.py: Figure 12(b)
  |- experimental
    |- distribution_classical.py, distribution_circular.py: Figure 16
    |- mean_classical.py, mean_circular.py: Figure 17
```

The above scripts will generate `.csv` files containing the results, which are also included in corresponding folders.
Then the PDF plots can be generated by running the scripts beginning with `draw_*` in the same folder.

## Limitations (Only for Functional and Reproduced badges)
In the quick reproduction, some figures are omitted due to minor parameter differences, for brevity. The fine-grained results can be found in the option 2.
