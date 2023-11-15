# Interface API

MiV-Simulator includes a more high-level interface built on [machinable](https://machinable.org) that can be useful in more custom use cases. 

For documentation on how to install and use machinable, please refer to the [machinable project website](https://machinable.org).

Here, we provide an example script that constructs the microcircuit simulation described in the previous sections. Additionally, we include a reservoir computing example that reproduces a classic seperation property experiment by [Maass et al. 2002](https://direct.mit.edu/neco/article/14/11/2531-2560/6650). This can serve as an illustration how to levarage the functional interface API.

In the `MiV-Simulator-Cases` repository, change into the `3-interface-api` directory and run `microcircuit.py` to construct the microcircuit NeuroH5. The `separation.py` script contains the full reservoir computing example.