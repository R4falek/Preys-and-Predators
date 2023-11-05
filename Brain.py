import torch.nn as nn
import torch
from torchviz import make_dot


class Brain(nn.Module):
    def __init__(self):
        super(Brain, self).__init__()
        self.fc1 = nn.Linear(10, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 3)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.sigmoid(self.fc3(x))
        return x

    def show_model(self, model, input_vector):
        vision_tensor = torch.tensor(input_vector, dtype=torch.float32).unsqueeze(0)
        dot = make_dot(model(vision_tensor), params=dict(model.named_parameters()))
        dot.render("my_network", format="png")
