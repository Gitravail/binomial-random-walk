# binomial-random-walk
A binomial random walk visualization program in python

# Required dependencies

* matplotlib : https://matplotlib.org/stable/users/installing/index.html
* numpy : https://numpy.org/install/
* scipy : https://scipy.org/install/

# UI

### Overview

Once the program is started the following UI shows up:

![Overview of the UI](images/overview.png)

### Figure view

On the left side a matplotlib plot window is displayed (empty at first).

![Figure view](images/figure.png)

To know more about how to use the plot interface please refer to :

* https://matplotlib.org/3.2.2/users/navigation_toolbar.html

### Control panel

The right panel contains the different parameters you can use and a plot button.

![Control panel](images/panel.png)

#### N slider

The N slider set the value of how many **random steps** must be performed on a **single** repetition.

A single repetition correspond to one random walk.

It's value range *between 10 and 100* (with 1 step)

#### REPEAT slider

The REPEAT slider set the value of how many **random walk**.

The purpose of this slider is to average the comportment of a single N step random walk.

It's value range *between 1000 and 100000* (with 1000 step)

#### q slider

The q slider set the value of the **probability the attacker success catching up by one block**.

It's value range *between 0 and 0.5* (with 0.01 step)

#### z slider

The z slider set the value of how many **block behind the trusted chain the attacker is**.

It's value range *between 1 and 100* (with 1 step)

#### Success probabilities results

The three labels shows theoritical computations in 1D of the success probability of the attacker to catch up according to *q* and *z*.

The first one shows is an estimation taking into account block verification and confirmation.

The second is the theoritical catching up value on the 1D random walk.

The third one is the actual catching up value on the 1D random walk.

#### 2D checkbox

This checkbox allows you to switch from a 1-D random walk to a 2-D random walk.
Both of them are recurrent since it is guaranteed to return to the starting position at some point (which is not in 3-D).

| 1-D                             | 2-D                             |
|---------------------------------|---------------------------------|
| ![1-D view](images/1d-view.png) | ![2-D view](images/2d-view.png) |

In black to the 1-D plot is added the interpolated curve to help you see the shape.

On both graph the red part is where the attacker managed to catch up.

#### PLOT button

The button used to display the random walk outcome according to the chosen parameters.

---

Author: Raphaël Tournafond