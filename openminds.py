class OpenMINDS:
    def __init__(self):
        for filename in Path('./openMINDS').glob('**/*.schema.json'):
            print(filename)
