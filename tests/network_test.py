"""
    Test the setup and evaluation of the networks
"""
import torch
from pseudo_backprop.network import FullyConnectedNetwork


class TestClassBackprop:
    """
        test the setup of a backprop network with one forward and
        one backwar step on synthetic data
    """

    def setUp(self):
        """set up an architecture and create a network"""
        self.layers = [200, 300, 320, 300, 10]
        self.backprop_net = FullyConnectedNetwork.backprop(self.layers)
        self.random_input = torch.randn(1, 200)
        self.random_output = torch.randn(1, 10)

    def forward_bpnetwork_test(self):
        """make a forward pass through the network""" 
        self.backprop_net(self.random_input)

    def backward_bpnetwork_test(self):
        """make a backward pass to calculate the gradients"""
        out = self.backprop_net(self.random_input)
        self.backprop_net.zero_grad()
        out.backward(self.random_output)


class TestClassFeedbackAlignement:
    """
        test the setup of a feeadback alignment network with one forward and
        one backwar step on synthetic data
    """

    def setUp(self):
        """set up an architecture and create a network"""
        self.layers = [200, 300, 320, 300, 10]
        self.fa_net = FullyConnectedNetwork.feedback_alignement(self.layers)
        self.random_input = torch.randn(1, 200)
        self.random_output = torch.randn(1, 10)

    def forward_feedbackalignement_test(self):
        """make a forward pass through the network""" 
        self.fa_net(self.random_input)

    def backward_feedbackalignement_test(self):
        """make a backward pass to calculate the gradients"""
        out = self.fa_net(self.random_input)
        self.fa_net.zero_grad()
        out.backward(self.random_output)
