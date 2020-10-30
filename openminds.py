import os.path
from pathlib import Path

class OpenMINDS:
    def __init__(self):
        for filename in Path('./openMINDS/v3.0/').glob('**/*.schema.json'):
            stripped_filename = os.path.splitext(
                                    os.path.splitext(
                                        os.path.basename(filename)
                                    )[0]
                                )[0]

            setattr(self, stripped_filename.upper(), stripped_filename)
