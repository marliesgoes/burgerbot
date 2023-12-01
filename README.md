# Talking to Robots: Burger Bot

## Setup

### 1. Install Required Packages

```bash
pip install -r requirements.txt
brew install ffmpeg
```

It takes a few more steps to install the visual modules. In the working directory, run:

```bash
# If you have already cloned the repo, maybe run `git submodule update --recursive --remote` to update the submodules
pip install -r Grounded-Segment-Anything/requirements.txt
pip install Grounded-Segment-Anything/GroundingDINO
pip install Grounded-Segment-Anything/segment_anything
```

Download the checkpoint

```bash
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth
```

### 2. Setup OpenAI API Key

Create a `.env` file in the project directory and add your OpenAI API key:

```.env
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Run the Script

```bash
python3 burgerbot.py
```