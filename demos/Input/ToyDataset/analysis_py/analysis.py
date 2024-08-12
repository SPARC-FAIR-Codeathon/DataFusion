import shutil

#####Import statements#######
import numpy as np
import pandas as pd
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import SimpleRNN, Dense
from tensorflow.keras.utils import to_categorical
############

####Add custom functions####
def create_model(input_shape, num_classes):
    model = Sequential()
    model.add(SimpleRNN(50, activation='relu', input_shape=input_shape))
    model.add(Dense(num_classes, activation='softmax'))
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model
########

### do not change the name of the file####
def run_analysis(filename): ## if using converted file, use this 

    # Load the data
    df = pd.read_csv('noisy_lfp_signals.csv') ## either the file you uploaded or the file that is created automatically after the conversion
    
    # Separate features and labels
    X = df.drop('Label', axis=1).values
    y = df['Label'].values
    
    # Normalize the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # labels to one-hot encoding
    y_one_hot = to_categorical(y)
    

    num_folds = 5
    kf = KFold(n_splits=num_folds, shuffle=True, random_state=0)
    results = []

    for fold, (train_index, test_index) in enumerate(kf.split(X_scaled)):

        X_train, X_test = X_scaled[train_index], X_scaled[test_index]
        y_train, y_test = y_one_hot[train_index], y_one_hot[test_index]
        
        # Reshape for RNN
        X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
        X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))
        
        # Create and train the model
        model = create_model(input_shape=(X_train.shape[1], 1), num_classes=y_one_hot.shape[1])
        model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=1)
        
        # Evaluate the model
        y_pred = model.predict(X_test)
        y_pred_classes = np.argmax(y_pred, axis=1)
        y_true_classes = np.argmax(y_test, axis=1)
        
        accuracy = accuracy_score(y_true_classes, y_pred_classes)
        results.append({'Fold': fold+1, 'Accuracy': accuracy})
    
        # save to csv
        results_df = pd.DataFrame(results)
        results_df.to_csv('rnn_cross_validation_results.csv', index=False)


    ### move all your files #### 
    command = "mkdir derived_analysis"
    subprocess.run(command, shell=True, check=True)    
    shuti.move("rnn_cross_validation_results.csv", "derived_analysis") ## do not change the destination
    #######

### do not change this ##
run_analysis(filename)