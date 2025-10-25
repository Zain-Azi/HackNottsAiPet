class Dragon:
    def __init__(self, name):
        self.__name = "Cheppie"
        self.__health = 1000
        self.__mood = "neutral"
        self.__action = "idle"

    def get_name(self):
        return self.__name
    
    def get_health(self):
        return self.__health
    
    def get_mood(self):
        return self.__mood
    
    def get_action(self):
        return self.__action
    
    def set_action(self, action):
        self.__action = action
    
    def set_name(self, name):
        self.__name = name

    def change_health(self, amount):
        self.__health += amount
        if self.__health > 1000:
            self.__health = 1000
        elif self.__health < 0:
            self.__health = 0
    
    def set_mood(self, mood):
        self.__mood = mood