# listener.py
# Basic Command Listener for Myko AI

class MykoAI:
    def __init__(self):
        self.active = False

    def listen(self, command: str) -> str:
        command = command.lower().strip()
        if command == "move":
            self.active = True
            return "Myko is moving..."
        elif command == "stop":
            self.active = False
            return "Myko has stopped."
        else:
            return f"Myko heard: {command}, but will wait."

# Example usage
if __name__ == "__main__":
    myko = MykoAI()
    print(myko.listen("move"))   # Activates Myko
    print(myko.listen("stop"))   # Deactivates Myko
    print(myko.listen("hello"))  # Acknowledges but does not act
