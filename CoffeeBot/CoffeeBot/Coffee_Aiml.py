import aiml
import os
path = 'C:/Users/vishnu.sk/Documents/Chatbot/CoffeeBot'
brain_file = "Coffee.brn"
os.chdir(path)

if __name__ == '__main__':
    kern = aiml.Kernel()
    kern.bootstrap(learnFiles=path+'/coffeebot.xml', commands="load aiml b")
    kern.saveBrain(brain_file)
    kern.bootstrap(brainFile=brain_file)
    while True:
        print (kern.respond(raw_input()))
