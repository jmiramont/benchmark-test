# A benchmark of signal denoising/ detection methods

[![Run benchmark](https://github.com/jmiramont/benchmark-test/actions/workflows/run_bm_denoising.yml/badge.svg)](https://github.com/jmiramont/benchmark-test/actions/workflows/run_bm_denoising.yml)
[![Results](docs/readme_figures/results_badge.svg)](results/readme.md)

[![Documentation](docs/readme_figures/docs_badge.svg)](https://jmiramont.github.io/benchmark-test/)

## Summary

- [A benchmark of signal denoising/ detection methods](#a-benchmark-of-signal-denoising-detection-methods)
  - [Summary](#summary)
  - [What is this benchmark?](#what-is-this-benchmark)
  - [How to use this benchmark?](#how-to-use-this-benchmark)
    - [Forking this repository](#forking-this-repository)
    - [Installation using ```poetry```](#installation-using-poetry)
  - [Benchmarking your own method](#benchmarking-your-own-method)
    - [Using a template file for your method](#using-a-template-file-for-your-method)
    - [Checking everything is in order with ```pytest```](#checking-everything-is-in-order-with-pytest)
    - [Create a pull request](#create-a-pull-request)
  - [Running this benchmark locally](#running-this-benchmark-locally)
    - [Configuring the benchmark parameters](#configuring-the-benchmark-parameters)
  - [Documenting your method](#documenting-your-method)

## What is this benchmark?

A benchmark is a comparison between different methods when running an standardized test. The goal of this benchmark is to compare different methods for denoising / detecting a signal based on different characterizations of the time-frequency representations. In particular, our goal is to evaluate the performance of techniques based on the zeros of the spectrogram and to contrast them with more traditional methods, like those based on the ridges of that time-frequency distribution.

Nevertheless, the methods to compare, the tests, and the performance evaluation functions were conceived as different modules, so that one can assess new methods without modifying the tests or the signals. On the one hand, the tests and the performance evaluation functions are encapsulated in the class `Benchmark`. On the other hand, the signals used in this benchmark are generated by the methods in the class `SignalBank`. The only restriction this poses is that the methods should satisfy some requirements regarding the *shape of their input an output parameters*.

The following block diagram depicts the relationship between the different block. The inward arrows represent the input of the user, who have to provide a number methods and (possibly) different parameters for them.
![Block Diagram](docs/readme_figures/block_diagram.svg)

## How to use this benchmark?

You can use this benchmark to test a new method against others. There are at least two ways of doing this:

1. You can either [make a new fork of this repository](#forking-this-repository) and make a pull request with a new method to test. A workflow using GitHub actions will automatically detect your new method and run the "standard" test.
2. You can clone this repository and [benchmark your own method locally](#running-this-benchmark-locally), i.e. in your computer. This will allow you to run the benchmark with all the modifications you want (type of signals, number of repetitions, etc.).

The [*notebooks*](./notebooks/) folder contains a number of minimal working examples to understand how this benchmark works and how you could use it for your project. In particular, [*demo_benchmark.ipynb*](./notebooks/demo_benchmark.ipynb) gives two minimal working examples to introduce the basic functionality of the `Benchmark` class, and the notebook [*demo_signal_bank.ipynb*](./notebooks/demo_signal_bank.ipynb) showcases the signals produced by the `SignalBank` class.

The instructions below will help you to add a new method and run the benchmark afterwards.

### Forking this repository

First you should have a local copy of this repository to add and modify files.
For this, [fork this repository](https://docs.github.com/en/get-started/quickstart/fork-a-repo), for example by using the "Fork" button above:

![Repository header](docs/readme_figures/header_repo.png)

This will create a copy of the repository in your own GitHub account, the URL of which should look like

```bash
https://github.com/YOUR-USERNAME/benchmark-test
```

Now, let's create a local copy, i.e. in your computer, of the repository you have just forked. Open a terminal in a directory of your preference and use

```bash
git clone https://github.com/YOUR-USERNAME/benchmark-test.git
```

When a repository is forked, a copy of all the branches existing in the original one are also created. It would be better if you create a new branch to work in your own changes, mainly adding your new method to be tested. For this, create a new branch using:

```bash
git branch new_method
git checkout new_method
```

### Installation using ```poetry```

*Remark for conda users:*

*If you have [`Anaconda`](https://www.anaconda.com/) or [`Miniconda`](https://docs.conda.io/en/latest/miniconda.html) installed please disable the auto-activation of the base environment and your conda environment using:*

```bash
conda config --set auto_activate_base false
conda deactivate
```

Before starting to make changes in the repository, we need to install the basic dependencies of the benchmark. With that in mind, we use [```poetry```](https://python-poetry.org/docs/), a tool for dependency management and packaging in python. First install ```poetry``` following the steps described [here](https://python-poetry.org/docs/#installation). Once you're done with this, open a terminal in the directory where you clone the benchmark (or use the console in your preferred IDE). Then, make ```poetry``` create a virtual environment and install all the current dependencies of the benchmark using:

```bash
poetry install 
```

Your method might need particular modules as dependencies that are not currently listed in the dependencies of the default benchmark. You can add all your dependencies by modifying the ```.toml``` file in the folder, under the ```[tool.poetry.dependencies]``` section. For example:

```bash
[tool.poetry.dependencies]
python = ">=3.8,<3.11"
numpy = "^1.22.0"
matplotlib = "^3.5.1"
pandas = "^1.3.5"
```

A more convenient and interactive way to do this interactively is by using ```poetry```, for example:

```bash
poetry add numpy
```

and following the instructions prompted in the console.

Afer this, run

```bash
poetry update
```

to update the .lock file in the folder.

*Remark: Notice that the use of ```poetry``` for adding the dependencies of your packet is key for running the benchmark using [GitHub Actions](./.github/workflows), please consider this while adding your method.*

## Benchmarking your own method

A new method can be tested against others by adding a file into the folder [src/methods](./src/methods) containing the definition of a class with some specific characteristics. We shall see how to do this in the following sections.

First, the function implementing your method must have the following signature:

```python
    def a_new_method(signals, params):
        ...
```

Methods should receive an `M`x`N` numpy array of signals, where `M` is the number of signals, and `N` is the number of their time samples. Additionally, they should receive a second parameter `params` to allow testing different combinations of input parameters. The shape and type of the output depends on the task (*denoising* or *detection*):

- For Denoising: The output must be a numpy array and have the same shape as the input (an array of shape `M`x`N`).
- For Detection: The output must be an array whose first dimension is equal to `M`.

In the following section, we will see how to create a class that compartmentalize your method and some information needed to run the benchmark.

### Using a template file for your method

The name of the file with your method must start with *method_* and have certain content to be automatically discovered by the benchmark functionality. For starters, the file should encapsulate your method in a new class. This is much easier than it sounds :). To make it simpler, [a file called *method_new_basic_template.py* is made available](./new_method_example/method_new_basic_template.py) which you can use as a template. You just have to fill in the parts that implement your method.

The template file *method_new_basic_template.py* is divided in three sections. In the first section, you can import a function with your method or implement everything in the same file:

```python
""" First section ----------------------------------------------------------------------
| Import here all the modules you need.
| Remark: Make sure that neither of those modules starts with "method_".
"""
from methods.MethodTemplate import MethodTemplate # Import the template!
```

Additionally, the [abstract class](https://docs.python.org/3/library/abc.html) `MethodTemplate` is imported here. Abstract classes are not implemented, but they serve the purpose of establishing a template for new classes, by forcing the implementation of certain *abstract* methods. We will see later that the class that encapsulates your method must inherit from this template.

The second section of the file should include all the functions your method needs to work. This functions could also be defined in a separate module imported in the previous section as well. Although it is not mandatory to add them here, but we recommend it so as to keep everything in a single file.

```python
""" Second section ---------------------------------------------------------------------
| Put here all the functions that your method uses.
| 
| def a_function_of_my_method(signal,params):
|   ...
"""
```

In the third and final section, your method is encapsulated in a new class called `NewMethod` (you can change this name if you prefer to, but it is not strictly necessary.). As mentioned before, the only requisite for the class that represents your method is that it inherits from the [abstract class](https://docs.python.org/3/library/abc.html) `MethodTemplate`. This simply means that you will have to implement the class constructor and a class function called -unsurprisingly- `method()`:

```python
""" Third section ----------------------------------------------------------------------
| Create here a new class that will encapsulate your method.
| This class should inherit the abstract class MethodTemplate.
| You must then implement the class function: 

def method(self, signal, params)
    ...
| which should receive the signals and any parameters that you desire to pass to your
| method.
"""

class NewMethod(MethodTemplate):
    def __init__(self):
        self.id = 'a_new_method'
        self.task = 'denoising'  # Should be either 'denoising' or 'detection'

    def method(self, signals, params = None): # Implement this method.
        ...

    # def get_parameters(self):            # Use it to parametrize your method.
    #     return [None,]

```

The constructor function ```__init__(self)``` must initialize the attributes ```self.id``` and ```self.task```. The first is a string to identify your method in the benchmark. The second is the name of the task your method is devoted to. This can be either ```'denoising'``` or ```'detection'```. Notice that if you fail to use such names this will prevent you from benchmarking your method.

Lastly, as anticipated above, you have to implement the class function ```method(self, signals, params)```. This function may act as a wrapper of your method, i.e. you implement your method elsewhere and call it from this function, or you could implement it directly here. This is up to you :).

If you want to test your method using different sets of parameters, you can also implement the function `get_parameters()` to return a list with the desired input parameters (you can find an example of this [here](./new_method_example/method_new_with_parameters.py)).

*Remark: Do not modify the abstract class `MethodTemplate`*.

Finally, **you have to move the file** with all the modifications to the folder [/src/methods](./src/methods). Changing the name of the file is possible, but keep in mind that **the file's name must start with "*method_*" to be recognizable**.

### Checking everything is in order with ```pytest```

Once your dependencies are ready, you should check that everything is in order using the ```pytest``` testing suit. To do this, simply run the following in a console located in your local version of the repository:

```bash
poetry run pytest
```

This will check a series of important points for running the benchmark online, mainly:

1. Your method class inherits the ```MethodTemplate``` abstract class.
2. The inputs and outputs of your method follows the required format according to the designated task.

Once the tests are passed, you can now either create a pull request to run the benchmark remotely, or [run the benchmark locally](#running-this-benchmark-locally).

### Create a pull request

In order to run the benchmark remotely, you can request the addition of your method for benchmarking along with other existing ones. This can be done by creating a [Pull Request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests). First, you need to update the remote version of your fork, now that you have added your new method and tested that it is working with ```pytest```. To do this, commit the changes and then push them to your remote repository:

```bash
git commit --all -m "Uploading a new method"
git push origin new_method
```

Now you can create a [new pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork) by using the "Contribute" button from the fork we have created before:

![Start a pull request.](docs/readme_figures/start_a_pull_request.png)

and then "Open a Pull Request". There you will need to select the branch where your changes are going to be made in the original repository of the benchmark. Please choose here "new_methods_branch":

![Choose the right branch.](docs/readme_figures/pull_request_branch.png)

Finally, send the pull request by clicking on "Create pull request":

![Create you pull request.](docs/readme_figures/finishing_pull_request.png)

You can also add an small comment in the "Write" field. A short explanation of the new method and related references (notes, articles, etc.) will be appreciated.

Once this is done, the benchmark is run remotely using [GitHub Actions](./.github/workflows) provided that the pull request is approved.

*Remark: Notice that ```pytest``` is also run again in this workflow. Therefore, keep in mind that if your method didn't pass the tests locally, it won't pass them at this stage either, and the pull request will not be approved*.

## Running this benchmark locally

Running the benchmark in your own computer can be useful if you want to use a different set of parameters of the experiments. In order to do this, you should update the configuration files `config_denoising.yaml` and `config_detection.yaml` with parameters of your choice.

### Configuring the benchmark parameters

In the configuration files you can change:

1. The length of the simulation.
2. The signals you use.
3. The number of times each simulation is run.
4. The signal-to-noise ratios (SNRs, in dB) used in each simulation.
5. The parallelization parameters (if needed).

The following example shows how to select a length of simulation of 512 time samples, with SNRs of 0, 10, 20 and 30 dB, repeating each experiment 30 times and using a parallel pool of five workers. Notice that the signals to use during the experiments are selected by the `signal_id` given by the `SignalBank` class (in this case, a linear chirp and an exponential chirp).

```yaml
# ------------------------------------------------------------------
# Configuration file for benchmarking denoising methods:
# ------------------------------------------------------------------
N: 512
SNRin: [0, 10, 20, 30]
repetitions: 30
parallelize: 5
signal_names: ['LinearChirp', 'ExpChirp',] # Use signal_id of SignalBank class.     
```

Once the configuration is ready, you can use the following command to run the benchmark using `poetry` (assuming [all you dependencies have been added to the `.toml` file and installed](#installation-using-poetry)):

```bash
poetry run python run_this_benchmark.py
```

## Documenting your method

For documenting your code, please add docstrings following [PEP257](https://peps.python.org/pep-0257/#:~:text=The%20aim%20of%20this%20PEP,conventions%2C%20not%20laws%20or%20syntax.). A docstring must be added at the beginning of the definition of classes and functions. The minimum information required is:

- Summary of the class/function.
- Brief description of input/output parameters.
- Any possible exception raised from your method.
