import shutil
import os

##### Import statements #######


############

#### Add custom functions ####


########

### Do not change the name of this function ###
def run_analysis(filename):  ## if using converted file, use this 

    # Load the data
    # df = pd.read_csv('noisy_lfp_signals.csv')  ## either the file you uploaded or the file that is created automatically after the conversion
    

    ### implement your analysis here ###


    ### Move all your files #### 
    command = "mkdir derived_analysis"
    os.system(command)  
    #########  


    ###### change file1,file2, file3, etc. to whatever your files that need to be stored are called 
    shutil.move(file1, "derived_analysis")  ## Do not change the destination
    shutil.move(file2, "derived_analysis")  ## Do not change the destination
