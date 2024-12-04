# Tim 7 CendekiAwan AI App: TemanTenang

Welcome to the Tim 7 CendekiAwan AI App! This AI-powered app uses Streamlit for a seamless client-server experience, all hosted on AWS.

[![Code Style: Google](https://img.shields.io/badge/code%20style-google-blue.svg)](https://google.github.io/styleguide/pyguide.html)
![pylint](https://img.shields.io/badge/Pylint-8.59-yellow?logo=python&logoColor=white)


## Getting Started

### Step 1: Clone the Repository

First, clone or fork this repository to your local machine. You’re just a few steps away from using the app!

### Step 2: Set Up a Virtual Environment

Run the following command to create a virtual environment:

```bash
python -m venv venv

```

### Step 3: Activate the Virtual Environment

Now, activate the virtual environment based on your operating system:

- On Windows: Run `.\venv\Scripts\activate`
- On Linux: Run `source venv/bin/activate`

### Step 4: Confirm Activation

To make sure your virtual environment is activated, run:

```bash
pip show pip
```

Check the `Location` in the output. If it shows a path within your venv, it’s active. This is a crucial step to ensure the app runs correctly.

### Step 5: Install Dependencies

Run the following command to install all necessary packages:

```bash
pip install -r requirements.txt
```

This may take a few minutes. Grab a cup of coffee while it installs! ☕

### Step 6: Get Your TogetherAI API Key

To power the app with AI, you’ll need an API key from TogetherAI. Sign up at [Together AI – Fast Inference, Fine-Tuning & Training](https://www.together.ai/)

### Step 7: Set Up Your `.env` File

Locate the `.env.sample` file in the project’s root directory. Rename it to `.env`, then open it and fill `TOGETHER_API_KEY` value with the key you received from TogetherAI.

### Step 8: Launch the App

You’re all set! Run the app with:

```bash
python -m streamlit run main.py
```

### Step 9: Enjoy

Your app will automatically open in your browser. Dive in and explore all the features!

<!-- 1. Clone or fork this repository.
1. Create a virtual environment with `python -m venv venv`
2. Then, activate the virtual environment depends on your operating system. 
   - For windows, run `.\venv\Scripts\activate`
   - Linux users, run `source venv/bin/activate`
3. Check if the virtual environment successfully activated. To check it, run `pip show pip` and inspect the `Location` path. If the Location in the output shows a path within your virtual environment, the venv is **active**. This is a crucial step, so make sure the virtual environment is activated.
4. Next, run `pip install -r requirements.txt` from your command line. This process might take a few minutes, so feel free to drink your coffee ☕.
5. After that, get your TogetherAI API Key by signing up to their website. So, visit [Together AI – Fast Inference, Fine-Tuning & Training](https://www.together.ai/)
6. Then, look for `.env.sample` file in the root directory of the project and rename it as `.env`
7. Next, open the `.env` file you previously renamed. Now, change the value of `TOGETHER_API_KEY` with your own api key.
8. Last, run the app with `python -m streamlit run main.py`
9.  Voila! It will automatically open your browser and shows the app. -->
