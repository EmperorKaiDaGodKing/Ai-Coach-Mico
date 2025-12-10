# Myko basic command listener (Python-style pseudocode)

class MykoAI:
    def __init__(self):
        self.active = False

    def listen(self, command):
        if command.lower() == "move":
            self.active = True
            return "Myko is moving..."
        elif command.lower() == "stop":
            self.active = False
            return "Myko has stopped."
        else:
            return f"Myko heard: {command}, but will wait."

# Example usage
myko = MykoAI()

print(myko.listen("move"))   # Activates Myko
print(myko.listen("stop"))   # Deactivates Myko
print(myko.listen("hello"))  # Just acknowledges
