Bayesian inference applied to chess — modelling position evaluation as a
probabilistic belief update.

Each move shifts a prior over who is winning into a posterior, and the
notebook walks through how the likelihood is built from engine evaluations,
how uncertainty shrinks as the game progresses, and where the model breaks
down in sharp tactical positions. Built in Pluto.jl.
