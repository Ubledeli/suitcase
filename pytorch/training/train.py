import os
import cv2
import pandas as pd
from torch import nn
from torch.optim import AdamW
from torch.optim.lr_scheduler import ReduceLROnPlateau
from torch.utils.data import Dataset, DataLoader, random_split
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm
import click
from datetime import datetime
import torch
import numpy as np

from pytorch.models.model import ResModel


class TrainDataset(Dataset):
    def __init__(self, path):
        folders = os.listdir(path)
        self.frames = pd.DataFrame()
        for folder in folders:
            images = os.listdir(f'{path}/{folder}/images')  # list of image paths
            labels = os.listdir(f'{path}/{folder}/labels')  # list of label paths
            frame = pd.DataFrame({'image': images, 'label': labels})
            self.frames = self.frames.append(frame, ignore_index=True)

    def __getitem__(self, item):
        img = cv2.imread(self.frames.at[item, 'image'])
        label = cv2.imread(self.frames.at[item, 'label'])
        return img, label

    def __len__(self):
        return len(self.frames)


@click.command(help="Train a model")
@click.option('--data_path', default='./train_set', help='Path to training data frames')
@click.option('--logdir', default='logs', help='Path to logging directory')
@click.option('--batch_size', default=16, help='batch size')
@click.option('--lr', default=1e-4, help='batch size')
@click.option('--name', default='exp-' + datetime.now().strftime("%d-%m-%Y-%H-%M-%S"))
def train(**options):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    logs_dir = os.path.join(options['logdir'], options['name'])
    weights_dir = os.path.join(logs_dir, "weights")
    os.makedirs(weights_dir, exist_ok=True)
    writer = SummaryWriter(log_dir=logs_dir)
    model = ResModel()
    dataset = TrainDataset(path=options['data_path'])
    lengths = [int(len(dataset) * 0.8), int(len(dataset)) - int(len(dataset) * 0.8)]
    train_dataset, test_dataset = random_split(dataset, lengths)
    train_dataloader = DataLoader(train_dataset, shuffle=True, batch_size=options['batch_size'], num_workers=0)
    test_dataloader = DataLoader(test_dataset, shuffle=True, batch_size=options['batch_size'], num_workers=0)

    model.cuda()
    # criterion = nn.L1Loss().cuda()
    criterion = nn.MSELoss().cuda()

    print(device)
    optimizer = AdamW(model.parameters(), options['lr'])
    scheduler = ReduceLROnPlateau(optimizer, 'min', factor=0.5, patience=3, verbose=True)
    best_test_loss = 1e7
    for i in range(391):
        epoch_loss = []
        model.train()
        for idx, train_data in enumerate(tqdm(train_dataloader, desc="Train")):
            img, label = train_data
            img = img.to(device)
            label = label.to(device).float()
            output = model(img)
            loss = criterion(output, label)
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
            epoch_loss.append(float(loss.item()))
            writer.add_scalar("TrainLoss", float(loss.item()), global_step=i * len(train_dataloader) + idx)

        model.eval()

        avg_loss = 0
        for idx, test_data in enumerate(tqdm(test_dataloader, desc="Test")):
            img, label = test_data
            img = img.to(device)
            label = label.to(device).float()
            output = model(img)
            loss = float(criterion(output, label).item())
            avg_loss += loss
            writer.add_scalar("TestLoss", loss, global_step=i * len(test_dataloader) + idx)

        avg_loss /= len(test_dataloader)
        writer.add_scalar("TestLossAvg", avg_loss, global_step=i * (len(test_dataloader) + 1))
        writer.add_scalar("TrainAverageLoss", np.mean(epoch_loss), global_step=i * (len(test_dataloader) + 1))
        writer.add_scalar("LR", optimizer.param_groups[0]['lr'], global_step=i)
        print(f"Epoch {i} loss: {np.mean(epoch_loss)}")
        scheduler.step(avg_loss)
        if best_test_loss > avg_loss:
            best_test_loss = avg_loss
            torch.save({"model": model.state_dict(),
                        "scheduler": scheduler.state_dict(),
                        "optimizer": optimizer.state_dict(),
                        "current_epoch": i}, f"{weights_dir}/best.pth")

        torch.save({"model": model.state_dict(),
                    "scheduler": scheduler.state_dict(),
                    "optimizer": optimizer.state_dict(),
                    "current_epoch": i}, f"{weights_dir}/latest.pth")


if __name__ == "__main__":
    cli = click.Group()
    cli.add_command(train)
    cli()
