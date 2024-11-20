# FAQs

`AI DIY Episode 2: Creating a Break Reminder App with ChatGPT` is available on [YouTube](https://youtu.be/uz46TR06CBs?si=Zmc7hkq4Czpq4wAR).

## What did you build in this episode?

In episode 2, we build a break reminder desktop application with ChatGPT that reminds us to take take short breaks every few hours while working and studying. This encourages us to get some fresh air or make a cup of coffee to avoid the negative effects of sitting in front of a computer screen all day.

<div style="display: flex; justify-content: space-between;">
    <img src="https://github.com/user-attachments/assets/59d0014e-d952-49c4-b38f-8976d0a2bc79" width="48%" alt="Break Reminder app interface on desktop">
    <img src="https://github.com/user-attachments/assets/0329075f-2ad3-4772-b8af-e3f31f620b3b" width="48%" alt="Break Reminder app 10-minute break alert while user is browsing the web">
</div>

## How do I make the Break Reminder App

### ChatGPT Prompt

I would suggest entering a prompt along these lines (please refine it as necessary for your needs):

`I want a programme that reminds me to take a 10 minute break every one or two hours. Every four hours I want the programme to remind me to take a 30 mins walk outside or have a lunch break. I want to come back from the break and know how long I have been away for. I then want to reset the timer for another one or two hours. I want the programme to have a simple and usable interface that allows me to easily view the timings and set the timer. I would like it to have a popup or alert function when it's time to take a break. I would like the programme to run on my desktop computer. I would like the code to be packaged so that it can run in an executable file. I want to only have to click on the executable file and it will run the programme until I choose to close it. I would like to be able to minimise and resize the interface. Can you give me the code for this programme?`

ChatGPT should give you the Python code to run in an executable file. Copy and paste the Python code into a file on your local computer. Save the file as `break_reminder.py`.

### Install Python (Mac users should be able to skip this step)

Check if Python is already installed by typing into the Terminal or Windows Command Prompt:

```
python --version
```

or possibly

```
python3 --version
```

If Python is not installed then you will need to first download Python from the [Python website](https://www.python.org/downloads/) (Python is free).

### Install Pyinstaller

After you have installed Python, install Pyinstaller (this will allow us to create the executable file) by typing into the Terminal:

```
pip install pyinstaller
```

or possibly

```
pip3 install pyinstaller
```

### Navigate to Python Script

Using the Terminal navigate to the directory where you have saved the Python file, i.e., whatever code from ChatGPT that you have copied and pasted into a local file:

```
cd path\to\your\script\folder
```

### Create executable with Pyinstaller

Once you have navigated in the Terminal to the folder containing your Python file create the executable with Pyinstaller

```
pyinstaller --onefile --windowed break_reminder.py
```

After running this command, go to the created `Dist` folder and there should be an executable file called `break_reminder.exe`. You can run the break reminder app by simply double clicking on this executable file. You can move the file to whatever location you wish. I moved it to my desktop folder.
