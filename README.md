# multiverse
User-friendly Bayesian Neural Networks (BNNs) using PyTorch and Pyro, built on top of [`TyXe`](https://github.com/TyXe-BDL/TyXe/tree/master) and extending it to the [linearized Laplace approximation](https://arxiv.org/abs/2008.08400). The implementation extends parts of the functionality of [`laplace`](https://github.com/AlexImmer/Laplace) to general likelihoods and priors.

**Inference methods:**
* Stochastic Variational inference (SVI): customize the variational posterior approximation as a Pyro guide, or use an Autoguide from `pyro.infer.autoguide.guides`.
* Linearized Laplace approximation (linLA): approximate the posterior with a Multivariate Normal, with covariance matrix built by inverting a generalized Gauss-Newton (GGN) approximation to the Hessian of the log-joint of data and parameters. Predicts by using the GLM predictive detailed in [Immer et al. (2021)](https://arxiv.org/abs/2008.08400) 
* MCMC: specify a Markov transition kernel to sample from the posterior of the parameters.

# Training, prediction, and evaluation
We begin by specifying an optimizer for the MAP, a neural architecture, a prior for the parameters, and a likelihood function (and, implicitly, a link function) for the response.
Simple neural architectures are provided in `BNNmultiverse.neural_nets`.

<<<<<<< HEAD
<<<<<<< HEAD
```
optim = pyro.optim.Adam({"lr": 1e-3})
net = multiverse.neural_nets.MLP(in_dim=1, out_dim=1, width=10, depth=2, activation="tanh")
=======
test

>>>>>>> 5403cd7 (test commit adding .gif to gitignore)

wp = .1 # prior precision for the parameters of the BNN
prior = multiverse.priors.IIDPrior((dist.Normal(0., wp**-2)))
I believe, the complete list of required dependencies, excluding the standard library (e.g., `os`) is:
=======

# Setup

## Setup steps using anaconda on MacOS

(on windows, I think the only difference is that you need to use `copy` instead of `cp`?)

0. Open the terminal and say `conda env list` to confirm that the code is not present already.

1. (_create an env with standard / easy-to-install packages_) `conda create --name bnns python=3.10 tqdm matplotlib numpy plotly scipy pip` (if desired, you can swap `bnns` for your preferred name).

2. (_activate the env for further installs_) `conda activate bnns`.

3. (_install pytorch_) This may depend on whether you want cuda, and on your conda channels. The simplest approach is: first try `conda install pytorch`. If that doesn't work (probably because channels) then try instead `pip install torch`.

4. (_install this code_) Navigate to wherever you want (e.g., the Documents folder), and clone this repo there. Then (mimicing [the SEPIA installation guidelines](https://sepia-lanl.readthedocs.io/en/latest/#installation)), "from the command line, while in the [the root depository of this repository], use the following command to install [bnns]:" `pip install -e .` "The -e flag signals developer mode, meaning that if you update the code from Github, your installation will automatically take those changes into account without requiring re-installation."

5. (_verify installation_) Try running one of the python files, e.g., `python scripts/SSGE_multivar_demo.py`, which should create a .gif of some histograms.


## Dependencies

Well, you need pytorch and matplotlib and such.
Perhaps non-trivially you need tqdm.
**Most notably,** you need my helper utils https://github.com/ThomasLastName/quality_of_life which you just need clone to anywhere on the path for your python environment (I got the impression from Natalie that y'all are allowed clone repos off the internet to your lanl devices? You need this repo)

I believe, the complete list of required dependencies, excluding the standard library (e.g., `typing`) is:
>>>>>>> 1892f43 (Minute tweaks to README)
- [ ] pytorch
- [ ] matplotlib
- [ ] tqdm
- [ ] numpy
- [ ] scipy
- [ ] plotly
- [ ] pyreadr
- [ ] https://github.com/ThomasLastName/quality-of-life (this repo has its own dependencies, but I believe it is sufficient to run this repo with only the above packages installed; I believe "the required parts" of this repo depend only on the same 5 packages as above and the standard python library).

If desired, the dependencies on `plotly` and `quality_of_life` could be removed.

# Usage

In order to run a test, the procedure is as follows. In order to specify hyperparameters, put a `.json` file containing hyperparameter values for the experiment that you want to run in the `experiments` folder.
Different algorithms require different hyperparmeters, and these differences are reflected in the scripts that load the `.json` files.
At the time of writing, there are 4 python scripts in the `experiments` folder: `bnn.py`, `det_nn.py`, `gpr.py`, and `stein.py`. To train a model with the hyperparamters specified by the `.json` file, say, `my_hyperpars.json`, you can run the script from the command in the experiment folder using `python <algorithm>.py --json my_hyperparameters`.
To see which hyperparameters are expected by the algorithm (which are the fields that you need to include in your .json file), check either the demo .json file included with the repo, or check the body the python script, where a dictionary called `hyperparameter_template` should be defined.

## Using the SLOSH Dataset

This only works if you have the file `slosh_dat_nj.rda` located in the `experiments` folder (not included with the repo!).

## Creating your own Dataset

All the .json files are supposed to have a field called "data" whose value is a text string. Suppose the "data" field has a value of "my_brand_new_dataset".
In that case, the python scripts which run experiments all attempt to `import my_brand_new_dataset from bnns.data` meaning that you need to create a file called `my_brand_new_dataset.py` located in the folder `data` if you want this to work.
Additionally, within that file `my_brand_new_dataset.py`, you must define 3 pytorch datasets: `D_train`, `D_val`, and `D_test`, as the python scripts which run experiments will attempt to access these variables from that file in that location.

## Creating your own Models

All the .json files are supposed to have a field called "model" whose value is a text string. Suppose the "model" field has a value of "my_brand_new_architecture".
In that case, the python scripts which run experiments all attempt to `import my_brand_new_architecture from bnns.data` meaning that you need to create a file called `my_brand_new_architecture.py` located in the folder `models` if you want this to work.
Additionally, within that file `my_brand_new_architecture.py`, you must define a pytorch model: either called `BNN` or called `NN` depending on the experiment that is being run

<<<<<<< HEAD
nprec = .1**-2 # noise precision for the likelihood function
likelihood = multiverse.likelihoods.HomoskedasticGaussian(n, precision=nprec)
```

For SVI and MCMC, see [TyXe](https://github.com/TyXe-BDL/TyXe/blob/master/README.md). For linLA, we can specify an approximation to the GGN approx. of the Hessian:
* `full` computes the full GGN
* `diag` computes a diagonal approx. of the GGN
* `subnet` considers `S_perc`% of the parameters having the highest posterior variance, as detailed in [Daxberger et al. (2021)](http://proceedings.mlr.press/v139/daxberger21a.html), to build a full GGN, fixing the other parameters at the MAP
For example:
```
bayesian_mlp = multiverse.LaplaceBNN(net, prior, likelihood, approximation='subnet', S_perc=0.5)
```

We can then train the model by calling:
```
num_epochs = 100
bayesian_mlp.fit(train_loader, optim, num_epochs)
```

Samples from the posterior in function space can be used to get samples from the posterior predictive:
```
f_samples = bayesian_mlp.predict(input_data, num_predictions=100)
y_samples = bayesian_mlp.likelihood.sample(f_predictions)
```
=======
>>>>>>> a95a0fe (added some usage instructions to README)


 - The code for SSGE was taken from the repo https://github.com/AntixK/Spectral-Stein-Gradient



# TODO

See the Issues tab.