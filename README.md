# PyCode
A simple framework in python for the analysis of MEA recordings

## Usage
To run the various tests and demo there is a powershell script *project.ps1*

``` pwsh
./project.ps1 help
```
to see the available commands

## Structure

The goal of the framework is to help analyze and visualize the data obtained
from MEA60 recordings during experiments with combined stimulation of 
ultrasounds and piezoelectric nanoparticles. Even if the goal is very specific,
i'm trying to keep the framework as generic as possible so it could be used on
other types of work too.

The whole framework works around some main structures that abstract the data of
the recordings: Signal, Phase and Experiment. A more detailed descriptions is
present (at the moment) only in the source code.

There are three main sections:

![](images/library_diagram.png)

* Convert data into an experiment representation
* Process and analyze an experiment
* Produce an output for visualize the results

## Coding convections

* Immutable structures: every structure is (for the most part, at least that 
  regarding the data of the recordings) immutable. So each method of the
  structure is granted to not modify itself, maybe just some metadata (at the
  moment).
  All function that produce a modified version of the data return a new
  structure that hold a copy of them so that the main typologies of flow in the
  code are:
  ``` python
    exp = Experiment()

    exp.info() # returns a str with the metadata of the experiment, exp.
    exp2 = apply(exp, operation) # return a new experiment with the result of
                                 # the applied operation
  ```
