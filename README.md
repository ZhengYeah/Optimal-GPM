# OGPM

[![arXiv](https://img.shields.io/badge/arXiv-2505.15483-<COLOR>.svg)](https://arxiv.org/abs/2505.15483)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Code for paper: [PETS'25] Optimal Piecewise-based Mechanism for Collecting Bounded Numerical Data under Local Differential Privacy

**Contributions:** 

* The first work to study the optimality of the piecewise-based mechanism under its most general form.
* The closed-form optimal mechanisms for classical domains and circular domains.

![img.png](others/poster.png)

## Code Structure

We encode the solving of the optimal $m$-piece mechanism under a distance metric as a *bilinear* optimization problem and solve it using the Gurobi solver.
The solving class for each distance metric can be found in the `src` folder.
Now we support the following distance metrics:
- $L_1$ distance (absolute error)
- $L_2$ distance (squared error)
- Wasserstein distance (a distribution distance, not used in the paper)

The main folders and files are as follows:

```
|- src (solving classes for different distance metrics and other mechanisms)
|- experiments (theoretical and experimental evaluations in the paper)
|- validation (validation of the optimal mechanism)
|- reproduction (quick reproduction of the results in the paper)
```

## Reproduction 

Tested environments: `uv` version `0.7.11` and Python version `3.12`~`3.13`.

**Install UV package manager.**
This project is packaged by `uv`, a modern Python package management system similar to `miniconda` or `poetry`.
All dependencies are listed in `pyproject.toml`.
We recommend using `uv` to create a virtual environment and install the dependencies.

![img.png](others/uv_official.png)

To install `uv`, follow the instructions in the "[uv installation](https://docs.astral.sh/uv/)".

After installation, follow the prompts to add `uv` to your system's `PATH`.
You can verify the installation by running the following command in your terminal (Windows, Linux, or macOS):

```
uv --version
```
This should display the installed version of `uv`.

**Install dependencies.**
After installing `uv`, cd to the project root directory and run:

```
[PROJECT_ROOT]$ uv sync
```

This command creates a virtual environment in the project root and installs the dependencies listed in `pyproject.toml`.
You can then run the provided scripts to reproduce the results in the paper. Two options are available:

### Option 1 (Quick) -- Recommended

The `reproduction` folder contains scripts  to reproduce key results from the paper. The structure is as follows:

```
|- reproduction
  |- figure_8_11.py: Figure 8a, 9a, 10a, 11b (Page 10)  (<1 minute)
  |- figure_12.py: Figure 12a and 12b (Page 11)  (<1 minute)
  |- figure_13_15.py: Figure 13a, 14, 15 (Page 11~12)  (<1 minute)
  |- figure_16_17.py: Figure 16a and 17a (Page 12)  (subsampled, <5 minutes)
```

You can run these scripts directly with `uv run` (no need to manually activate the environment).
For example, to generate the first group of figures:

```
[PROJECT_ROOT]$ uv run ./reproduction/figure_8_11.py
```

You can also specify a tested Python version (e.g. Python 3.13):

```
[PROJECT_ROOT]$ uv run --python 3.13 ./reproduction/figure_8_11.py
```

This will display the corresponding figures using matplotlib.

Some figures are omitted due to minor parameter differences, for brevity.
The last script is a subsampled version of the original one to speed up the reproduction.
It may slightly differ from the original figure in the paper, but the overall trend remains the same.
The fine-grained results can be obtained by running the scripts in the `experiments` folder.

### Option 2 (Detailed)

The `experiments` folder contains all scripts used in the paper, including intermediate results and full figures. These scripts rely on PyCharm’s path configuration. To run them, you need the PyCharm GUI and run them by right-clicking the script.

If you have installed `uv`, you can select it as the interpreter in PyCharm. PyCharm will then automatically create a virtual environment and install all dependencies specified in `pyproject.toml`.
For detailed instructions, see the official guide: [PyCharm: configure a uv environment](https://www.jetbrains.com/help/pycharm/uv.html).

After setting up the environment, there should be no package import errors. Then you can run the scripts by opening them and right-clicking in the PyCharm editor and selecting "Run `file_name.py`".

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


