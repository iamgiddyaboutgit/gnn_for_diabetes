from torch_geometric.nn import GraphConv
import torch.nn.functional as F
from torch_geometric.nn import global_mean_pool
from torch.nn import Linear
import torch

class GNN(torch.nn.Module):
    def __init__(self, input_size, hidden_size_1, hidden_size_2, hidden_size_3, output_size):
        super(GNN, self).__init__()
        hidden_size = hidden_size_1
        hidden_size_2 = hidden_size_2
        hidden_size_3 = hidden_size_3
        self.conv1 = GraphConv(input_size, hidden_size)
        self.conv2 = GraphConv(hidden_size, hidden_size_2)
        self.conv3 = GraphConv(hidden_size_2, hidden_size_3)
        self.fc1 = Linear(hidden_size_3, hidden_size)
        self.fc2 = Linear(hidden_size, output_size)

    def forward(self, x, edge_index, batch):
        # TODO: Finish this function
        x = F.relu(self.conv1(x, edge_index))
        x = F.dropout(x, training=self.training)
        x = F.relu(self.conv2(x, edge_index))
        x = F.dropout(x, training=self.training)
        x = F.relu(self.conv3(x, edge_index))
        # x = F.dropout(x, training=self.training)
        x = global_mean_pool(x, batch)
        x = self.fc1(x)
        x = self.fc2(x)
        return x