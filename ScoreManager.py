import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class ScoreManager():

    """Class reading the highscore and saving the newest highscore to a file."""

    def __init__(self):
        
        self.high_score = 0

    def add(self, score):

        with open(os.path.join(BASE_DIR, 'Media', 'scores.txt'), 'r') as f:

            line = f.readline().strip()
            if line.isdigit():
                existing_score = int(line)
            else:
                existing_score = 0
                    
        if score > existing_score:
            with open(os.path.join(BASE_DIR, 'Media', 'scores.txt'), 'w') as f:
                f.write(str(score))

    def reset(self):

        with open(os.path.join(BASE_DIR, 'Media', 'scores.txt'), 'w') as f:
            f.write("0")
