import random
from collections import defaultdict, Counter
import nltk
from nltk.tokenize import word_tokenize, RegexpTokenizer
import os

def run_only_once():
    file_path = "run_only_once.txt"
    
    # Check if the file exists
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            content = f.read().strip()
            if content == "true":
                print("Action already performed, skipping.")
                return

    nltk.download('punkt')    
    with open(file_path, "w") as f:
        f.write("true")
    print("Action completed and recorded.")

# Call the function
run_only_once()


class MarkovChain:
    def __init__(self, n=2):
        self.n = n
        self.model = defaultdict(Counter)
        self.iter_list = []
        

    def clean_text(slef, text):
        text = text.lower()    
        tokenizer = RegexpTokenizer(r'\w+')
        words = tokenizer.tokenize(text)
        return words
    
    def train(self, text):
        text = text.lower().strip()
        for i in range(len(text) - self.n):
            gram = text[i:i+self.n]
            next_char = text[i+self.n]
            self.model[gram][next_char] += 1
    
    def predict_next_char(self, current_gram):
        if current_gram in self.model:
            total_occurrences = sum(self.model[current_gram].values())
            probs = {char: count / total_occurrences for char, count in self.model[current_gram].items()}
            next_char = random.choices(list(probs.keys()), list(probs.values()))[0]
            return next_char, probs
        else:
            return None, None
    
    def iterative_char_prediction(self, start_text, min_iter=5):
        current_text = start_text
        
        for _ in range(min_iter):
            current_gram = current_text[-self.n:]
            next_char, _ = self.predict_next_char(current_gram)
            if next_char is None:
                break
            current_text += next_char
            print(f"Current text: {current_text}")
            self.iter_list.append(current_text)
        
        return current_text, self.iter_list
    
    def build_markov_chain(self, text, n=2):
        model = defaultdict(lambda: defaultdict(int))
        words = self.clean_text(text) 

        for i in range(len(words) - n):
            gram = tuple(words[i:i + n])
            next_word = words[i + n]
            model[gram][next_word] += 1

        # Convert counts to probabilities
        for gram, transitions in model.items():
            total = float(sum(transitions.values()))
            for next_word in transitions:
                model[gram][next_word] /= total

        return model

    # Function to generate text
    def generate_text(self, model, start_text, length=100):
        n = len(list(model.keys())[0])
        current_gram = tuple(self.clean_text(start_text)[:n])
        result = list(current_gram)

        for _ in range(length):
            if current_gram not in model:
                break
            next_word = random.choices(list(model[current_gram].keys()),
                                    list(model[current_gram].values()))[0]
            result.append(next_word)
            current_gram = tuple(result[-n:])

        return ' '.join(result)
# "Arduino is an open-source electronics platform based on easy-to-use hardware and software"
def run_mkov(text, n_grams_char, start_text_char, min_iter, model_question, length=50):
    markov = MarkovChain(n=n_grams_char)
    markov.train(text)
    final_text, lst = markov.iterative_char_prediction(start_text_char, min_iter)
    print(f"Final generated text: {final_text}")
    
    word_model = markov.build_markov_chain(text)
    generated_text = markov.generate_text(word_model, model_question, length)
    print("Generated Text:\n", generated_text)
    return final_text, lst,  generated_text

if __name__ == "__main__":
    text = """Arduino is an open-source electronics platform based on easy-to-use hardware and software. It's designed to make electronics more accessible to artists, designers, hobbyists, and anyone interested in creating interactive projects. The core of the Arduino platform is the Arduino board, a small microcontroller that can be programmed to sense and control objects in the physical world.

The Arduino platform has gained immense popularity due to its simplicity and versatility. It allows users to create projects ranging from simple LED blinkers to complex home automation systems. The beauty of Arduino lies in its ability to bridge the gap between software and hardware, enabling even those without a background in electronics to bring their ideas to life.

At the heart of an Arduino board is a microcontroller, a small computer on a single integrated circuit that contains a processor, memory, and input/output peripherals. The most common microcontroller used in Arduino boards is the ATmega328, but other boards use different microcontrollers with varying capabilities. The microcontroller is responsible for executing the code uploaded to it and interacting with the physical world through sensors, actuators, and other electronic components.

Programming an Arduino board is done through the Arduino Integrated Development Environment (IDE), a free and open-source software application that allows users to write, compile, and upload code to the board. The code, often referred to as a "sketch," is written in a simplified version of C/C++ and is designed to be easy to learn and use. The Arduino IDE also includes a vast library of code examples and references, making it easier for beginners to get started.

One of the most powerful aspects of Arduino is its community. Over the years, a large and active community of developers, enthusiasts, and educators has formed around Arduino, creating a wealth of resources, tutorials, and projects that are freely available online. This community-driven approach has led to the development of countless Arduino-compatible boards, shields, and modules, expanding the platform's capabilities and allowing users to find solutions tailored to their specific needs.

Arduino boards come in various shapes and sizes, each designed for different applications. The most well-known board is the Arduino Uno, which is a general-purpose board suitable for most projects. Other popular boards include the Arduino Nano, a smaller version of the Uno; the Arduino Mega, which offers more input/output pins and memory for more complex projects; and the Arduino Leonardo, which can emulate a keyboard or mouse.

In addition to the hardware, Arduino also supports a wide range of sensors, actuators, and other components that can be easily connected to the board. These components allow Arduino to interact with the physical world in various ways, such as measuring temperature, detecting motion, controlling motors, and more. This flexibility makes Arduino an ideal platform for prototyping and experimentation.

One of the key strengths of Arduino is its ability to interface with other devices and platforms. Arduino can communicate with computers, smartphones, and other microcontrollers, allowing users to create interconnected systems and IoT devices. For example, an Arduino board can be used to collect data from sensors and send it to a computer for analysis, or it can receive commands from a smartphone to control home appliances.

Arduino is also widely used in education, where it serves as a tool for teaching electronics, programming, and robotics. Its simplicity and hands-on approach make it an excellent choice for introducing students to STEM (Science, Technology, Engineering, and Mathematics) concepts. Many educational institutions around the world use Arduino in their curricula, and numerous educational kits and resources are available to support this.

In conclusion, Arduino is a versatile and accessible platform that has revolutionized the way people interact with electronics. Whether you're a beginner looking to learn the basics of programming and electronics or an experienced engineer developing complex projects, Arduino offers a powerful toolset that can help bring your ideas to life. Its open-source nature, combined with a strong community and a wide range of compatible components, makes it a valuable resource for anyone interested in exploring the world of electronics and embedded systems."""
    run_mkov(text, 3, "ard", 5, "Arduino is an open-source electronics platform based on easy-to-use hardware and software", 50)