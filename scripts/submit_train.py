#!/home/postulka/programs/anaconda3/envs/tf_2-6/bin/python

import argparse
from gmnn.trainer import PESTrainer

def parse_arguments():
    """Parse command-line arguments for the training config."""
    parser = argparse.ArgumentParser(description="Submit training job")
    parser.add_argument("--config", help="Path to the training config file", required=True)
    return parser.parse_args()

if __name__ == '__main__':
    # Parse the command-line arguments
    args = parse_arguments()

    # Initialize the PESTrainer with the config file
    trainer = PESTrainer(config=args.config)

    # Start the training process
    trainer.fit()

    # Evaluate the trained model
    trainer.eval()

