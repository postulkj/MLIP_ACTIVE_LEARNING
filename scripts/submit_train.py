#!/home/postulka/programs/anaconda3/envs/tf_2-6/bin/python

from gmnn.trainer import PESTrainer

if __name__ == '__main__':

    # Initialize the PESTrainer with the config file
    trainer = PESTrainer(config="temp_config.txt")

    # Start the training process
    #trainer.fit()

    # Evaluate the trained model
    trainer.eval()

