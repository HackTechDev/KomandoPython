class Way():
    fromx = 0
    fromy = 0
    level = ""
    tox = 0
    to = 0    
    def __init__(self, value):
        position = value.split(",")        
        self.fromx = int(position[0]) 
        self.fromy = int(position[1]) 
        self.level = position[2]
        self.tox = int(position[3])
        self.toy = int(position[4])
