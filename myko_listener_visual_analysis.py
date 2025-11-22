# myko_listener.py
# Myko AI Listener with Visual Analysis

from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

class MykoAI:
    def __init__(self):
        self.active = False
        # Load BLIP model for image captioning
        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

    def listen(self, command: str, file_path: str = None) -> str:
        command = command.lower().strip()

        if command == "move":
            self.active = True
            return "Myko is moving..."
        elif command == "stop":
            self.active = False
            return "Myko has stopped."
        elif command == "analyze photo":
            if file_path:
                return self.describe_image(file_path)
            else:
                return "No photo provided to analyze."
        else:
            return f"Myko heard: {command}, but will wait."

    def describe_image(self, image_path: str) -> str:
        image = Image.open(image_path).convert("RGB")
        inputs = self.processor(images=image, return_tensors="pt")
        out = self.model.generate(**inputs)
        caption = self.processor.decode(out[0], skip_special_tokens=True)
        return f"Myko sees: {caption}"

# Example usage
if __name__ == "__main__":
    myko = MykoAI()
    print(myko.listen("move"))
    print(myko.listen("stop"))
    print(myko.listen("analyze photo", "your_photo.jpg"))
