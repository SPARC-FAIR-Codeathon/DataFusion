import shutil
import os

##### Import statements #######
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
############

#### Add custom functions ####
class SimpleRNNModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(SimpleRNNModel, self).__init__()
        self.rnn = nn.RNN(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)
    
    def forward(self, x):
        out, _ = self.rnn(x)
        out = self.fc(out[:, -1, :])
        return out

def create_model(input_size, hidden_size, output_size):
    model = SimpleRNNModel(input_size, hidden_size, output_size)
    return model

def normalize_features(X):
    mean = np.mean(X, axis=0)
    std = np.std(X, axis=0)
    X_normalized = (X - mean) / std
    return X_normalized

def cross_validation_split(X, y, num_folds):
    fold_size = len(X) // num_folds
    indices = np.arange(len(X))
    np.random.shuffle(indices)
    folds = [(indices[i*fold_size:(i+1)*fold_size], np.concatenate((indices[:i*fold_size], indices[(i+1)*fold_size:])))
             for i in range(num_folds)]
    return folds

def calculate_accuracy(y_true, y_pred):
    correct_predictions = torch.sum(y_true == y_pred)
    total_predictions = len(y_true)
    accuracy = correct_predictions.float() / total_predictions
    return accuracy.item()


########

### Do not change the name of this function ###
def run_analysis(filename):  ## if using converted file, use this 

    # Load the data
    df = pd.read_csv('noisy_lfp_signals.csv')  ## either the file you uploaded or the file that is created automatically after the conversion
    
    # Separate features and labels
    X = df.drop('Label', axis=1).values
    y = df['Label'].values
    
    # Normalize the features
    X_scaled = normalize_features(X)
    
    # Convert labels to tensor
    y_tensor = torch.tensor(y, dtype=torch.long)
    
    num_folds = 2
    results = []
    folds = cross_validation_split(X_scaled, y_tensor, num_folds)

    for fold, (test_index, train_index) in enumerate(folds):

        X_train, X_test = X_scaled[train_index], X_scaled[test_index]
        y_train, y_test = y_tensor[train_index], y_tensor[test_index]
        
        # Convert to torch tensors
        X_train = torch.tensor(X_train, dtype=torch.float32).unsqueeze(-1)
        X_test = torch.tensor(X_test, dtype=torch.float32).unsqueeze(-1)
        
        # Create DataLoader
        train_dataset = TensorDataset(X_train, y_train)
        test_dataset = TensorDataset(X_test, y_test)
        train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
        test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)
        
        # Create and train the model
        input_size = X_train.shape[2]
        hidden_size = 10
        output_size = len(torch.unique(y_tensor))
        model = create_model(input_size, hidden_size, output_size)
        
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=0.001)
        
        for epoch in range(5):
            model.train()
            for batch_X, batch_y in train_loader:
                optimizer.zero_grad()
                outputs = model(batch_X)
                loss = criterion(outputs, batch_y)
                loss.backward()
                optimizer.step()
        
        # Evaluate the model
        model.eval()
        all_preds = []
        with torch.no_grad():
            for batch_X, _ in test_loader:
                outputs = model(batch_X)
                _, predicted = torch.max(outputs, 1)
                all_preds.append(predicted)
        
        y_pred_classes = torch.cat(all_preds)
        accuracy = calculate_accuracy(y_test, y_pred_classes)
        results.append({'Fold': fold+1, 'Accuracy': accuracy})
    
    # Save to CSV
    results_df = pd.DataFrame(results)
    results_df.to_csv('rnn_cross_validation_results.csv', index=False)
    
    ## Save the model code for just 1 fold
    torch.save(model.state_dict(), f'rnn_model_fold_5.pth')

    ### Move all your files #### 
    command = "mkdir derived_analysis"
    os.system(command)    

    shutil.move("rnn_cross_validation_results.csv", "derived_analysis")  ## Do not change the destination
    shutil.move("rnn_model_fold_5.pth", "derived_analysis")  ## Do not change the destination