# School Project: Covid-19 Death Prediction Model Server

## Overview
This school project simulates machine learning by predicting the number and pattern of deaths caused by covid-19 overtime based on given data. The application utilizes Stochastic Gradient Descent to train a PyTorch model and the model server uses multiple threads and caches the predictions (to save effort when the server is given the same inputs repeatedly). Additionally, the model server runs in a Docker container and receives requests over a network (via gRPC calls).

## Functionality
Stochastic Gradient Descent: a simple yet very efficient approach to fitting linear classifiers and regressors under convex loss functions such as (linear) Support Vector Machines and Logistic Regression.

gRPC: a modern open source high performance Remote Procedure Call (RPC) framework that can run in any environment. It can efficiently connect services in and across data centers with pluggable support for load balancing, tracing, health checking and authentication. It is also applicable in last mile of distributed computing to connect devices, mobile applications and browsers to backend services.

Docker container: a standard unit of software that packages up code and all its dependencies so the application runs quickly and reliably from one computing environment to another. 
