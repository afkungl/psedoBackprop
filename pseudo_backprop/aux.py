"""Standalone functions for auxillary computations."""
import numpy as np
import torch


def evaluate_model(network_model, testloader, batch_size, device='cpu',
                   nb_classes=10):
    """
    Evaluate the model on the given dataset and obtain the loss function and
    the results

    Params:
        network_model: FullyConnectedNetwork object containing the neural
                       network
        testloader: the testloader object from torch
        batch_size: batch size
        device (str, optional): 'gpu' or 'cpu' according to the availability

    Returns:
        loss: the computed loss value
        confusion_matrix: numpy matrix with the confusion matrix
    """
    # pylint: disable=R0914

    confusion_matrix = np.zeros((nb_classes, nb_classes))
    loss_function = torch.nn.MSELoss(reduction='sum')
    y_onehot = torch.empty(batch_size, nb_classes, device=device)
    y_onehot.to(device)
    loss = 0
    # turn off gathering the gradient for testing
    with torch.no_grad():
        for data in testloader:
            images, labels = data[0].to(device), data[1].to(device)
            images = images.float()     # for yinyang, we need to convert to float32
            images = images.view(batch_size, -1)
            outputs = network_model(images)
            y_onehot.zero_()
            unsq_label = labels.unsqueeze(1)
            y_onehot.to(device)
            unsq_label.to(device)
            y_onehot.scatter_(1, unsq_label, 1)
            loss_value = loss_function(outputs, y_onehot)
            loss += loss_value
            _, predicted = torch.max(outputs, 1)
            for tested in \
                zip(labels.clone().detach().cpu().numpy().astype(int),
                    predicted.clone().detach().cpu().numpy().astype(int)):
                confusion_matrix[tested] += 1

    return loss, confusion_matrix


def generalized_pseudo(w_matrix, dataset):
    """calculate the dataspecific pseudoinverse

    Args:
        w_matrix (torch.tensor): forward matrix
        dataset (torch.tensor): dataset
    """

    np_dataset = dataset.detach().cpu().numpy()
    covariance = np.cov(np_dataset.T)
    mean = np.mean(np_dataset, axis=0)
    gammasquared = covariance + np.outer(mean,mean)
    
    # make the singular value decomposition
    u_matrix, s_matrix, vh_matrix = np.linalg.svd(gammasquared)
    # Calculate the generalized pseudoinverse
    gamma = np.dot(np.dot(u_matrix, np.diag(np.sqrt(s_matrix))), vh_matrix)
    gen_pseudo = np.dot(gamma, np.linalg.pinv(np.dot(w_matrix, gamma)))

    return torch.from_numpy(gen_pseudo)


def calc_gamma_matrix(dataset):
    """calculate square root of the
       autocorrelation Gamma^2 = <rr^T>

    Args:
        dataset (torch.tensor): dataset r
        (tensor of data vectors r)
    """

    np_dataset = dataset.detach().cpu().numpy()
    covariance = np.cov(np_dataset.T)
    mean = np.mean(np_dataset, axis=0)
    gammasquared = covariance + np.outer(mean,mean)
    # print('mean: ', mean)
    # print('cov:', covariance)
    
    # make the singular value decomposition
    u_matrix, s_matrix, vh_matrix = np.linalg.svd(gammasquared)
    # Calculate the generalized pseudoinverse
    gamma = np.dot(np.dot(u_matrix, np.diag(np.sqrt(s_matrix))), vh_matrix)

    return torch.from_numpy(gamma)


def calc_loss(b_matrix, w_matrix, samples):
    """Calculate the loss based on the samples
    Args:
        b_matrix (np.ndarray): The backward matrix
        w_matrix (np.ndarray): The forward matrix
        samples : Samples to calcualte over
    Returns:
        float: the calculated loss
    """
    b_matrix = np.reshape(b_matrix, w_matrix.T.shape)
    bw_product = b_matrix.dot(w_matrix.dot(samples))
    diff = samples - bw_product
    f_samples = np.sum(np.power(diff, 2), axis=0)
    loss = np.mean(f_samples)

    return loss


def calc_activities(network, inputs, nb_layers):
    """calculate the activities throughout a network

    Args:
        network (network class): Description
        input (inout data): Description
        nb_layers (number of layers): Description
    """

    activities = []
    for layer in range(nb_layers):
        activities.append(
            network.forward_to_hidden(inputs, layer).detach().numpy())

    return activities

def calc_mismatch_energy(Gamma, B, W):
    """calculates the mismatch energy between B
       and the data-specific pseudoinverse of W

    Args:
        Gamma: square root of data vector
        B: backwards matrix
        W: forwards matrix

        all as numpy arrays
    """

    mismatch_energy = .5 * np.linalg.norm(Gamma - B @ W @ Gamma)

    return mismatch_energy
