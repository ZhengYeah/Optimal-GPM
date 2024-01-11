import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
import pandas as pd


class DP_Dataset(Dataset):
  
    def __init__(self, csv_file, transform=None):
        self.data_frame = pd.read_csv(csv_file)
        self.transform = transform

    def __len__(self):
        return len(self.data_frame)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        input_frame = self.data_frame.iloc[idx, 2]
        label = self.data_frame.iloc[idx, 0]
        sample = {"input": input_frame, "label": label}
        if self.transform:
            sample = self.transform(sample)
        return sample

dp_dataset = DP_Dataset("PM_on_discretization.csv")
# for i, sample in enumerate(dp_dataset):
#         print(i, sample["training"], sample["label"])

batch_size = 1000

train_loader = DataLoader(dp_dataset, batch_size=batch_size, shuffle=False, pin_memory=True)
test_loader = DataLoader(dp_dataset, batch_size=batch_size * 10, shuffle=False, pin_memory=True)


def dp_attack_ffnn():
    model = nn.Sequential(
        nn.Linear(1, 50),
        nn.ReLU(),
        nn.Linear(50, 50),
        nn.ReLU(),
        nn.Linear(50, 50),
        nn.ReLU(),
        nn.Linear(50, 50),
        nn.ReLU(),
        nn.Linear(50, 50),
        nn.ReLU(),
        nn.Linear(50, 50),
        nn.ReLU(),
        nn.Linear(50, 50),
        nn.ReLU(),
        nn.Linear(50, 50),
        nn.ReLU(),
        nn.Linear(50, 50),
        nn.ReLU(),
        nn.Linear(50, 20),
    )
    return model


model = dp_attack_ffnn()
num_epochs = 100


def train(model, train_loader):
    criterion = torch.nn.CrossEntropyLoss()
    # optimizer = torch.optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
    optimizer = torch.optim.Adam(model.parameters(), lr=3e-4)

    for epoch in range(num_epochs):
        batch_loss = 0
        total_batches = 0

        for i, samples_batch in enumerate(train_loader):
            # print(i, samples_batch["input"].size(), samples_batch["label"].size())
            training_input = samples_batch["input"].reshape(-1, 1)
            training_input = training_input.type(torch.float32)
            labels = samples_batch["label"]
            labels = labels.type(torch.LongTensor)
            outputs = model(training_input)
            loss = criterion(outputs, labels)
            # Backward and optimize
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()   

            total_batches += 1     
            batch_loss += loss.item()

        avg_loss_epoch = batch_loss / total_batches
        print('Epoch [{}/{}], Averge Loss:for epoch[{}, {:.4f}]'.format(epoch + 1, num_epochs, epoch + 1, avg_loss_epoch))

    torch.save(model.state_dict(), './dp_attack_ffnn.pth')


def accuracy_test(model_path, test_loader):
    # correct = 0
    # total = 0

    model = dp_attack_ffnn()
    model.load_state_dict(torch.load(model_path))

    with torch.no_grad():
        for samples_batch in test_loader:
            training_input = samples_batch["input"].reshape(-1, 1)
            training_input = training_input.type(torch.float32)
            outputs_test = model(training_input)
            labels = samples_batch["label"]
            labels = labels.type(torch.LongTensor)
            _, predicted = torch.max(outputs_test.data, 1)
            # print(predicted)
            # total += labels.size(0)

            discretization_delta = 0.05
            absolute_error = torch.abs(predicted - labels) * discretization_delta
            absolute_error = torch.mean(absolute_error)

            print(f"Mean absolute error of the 1000 test cases: {absolute_error}")


if __name__ == '__main__':
    train(model, train_loader)
    accuracy_test("dp_attack_ffnn.pth", test_loader)

