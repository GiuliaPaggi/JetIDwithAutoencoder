# Jet Identification with autoencoder
Train an autoencoder to classify jet like events in CMS DTs.


## General Information
The aim of this project is to use an encoder and a fully connected layer to perform a classification of shower events in CMS Drift Tube chambers, in particular using information from the two phi superlayers.
The simulated data describes the decay of a heavy neutral particle produced in gluon gluon fusion with 375 GeV mass and decay on average after 1 m in the CMS detector.
First, an autoencoder is trained with a set of selected shower events. To achieve better results in fewer training epochs, a exponential decay schedule is implemented to progressively reduce the learning rate and an early stop mechanism that stops the train after 10 epochs in which the loss value is larger or equal to the previous epoch value.
The second part implements a fully connected layer to classify the imput as shower or not.
To build a classification network, the encoder part of the trained autoencoder is used to reduce the dimensionality of each input in the training dataset. Also in this case, the same learining rate schedule and early stopping mechanism are used.
After the training, an accuracy of 98.8% on the test set is obtained.

## Structure of the project
The project is divided in the following way:
- **digi_preprocess_list.py**:  reads the simulated Ntuple, performs the selection of showers (defines as events with at least 40 channels fired) and muon (6 < channels fired < 15 ) and writes the selected events in csv files to  be used in the training;
- **JetIDwithAutoencoder.py**: google colab notebook with the autoencoder and the subsequent classification layer definition, training and test;

Since the available data was not enough, a data augmentation strategy was employed. For each shower event, copies are created by shifting the entire shower one channel at the time both left and right, as long as the entire event is still contained. 
For muon events, the same is performed with half of the original events.

The preprocessed data can be found at: https://drive.google.com/drive/folders/1p4OJ5rba62HQGJEz4uIv__Z-mPrIDGhE?usp=drive_link

