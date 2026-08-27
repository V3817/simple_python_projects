import os 
if __name__=="__main__":
    print("Welcome Guys if you cannot speak then type the system will speak aloud")
    while(True):
        sentence=input("Enter the sentence here : ___ or press (q or Q) to exit")
        if sentence.lower()== "q":
            break
        command = f'''PowerShell -Command "Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('{sentence}');"'''
        os.system(command)
    print("Thanks for using this ,hope we will meet soon!")    



