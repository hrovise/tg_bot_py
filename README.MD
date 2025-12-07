🤖 Telegram Meme Generator Bot
Bot draws text on an image at the bottom from one to two lines(default:black color, can be customized 
by setting white color)

Description

Bot will burn the text onto the image using the `DejaVuSans` font.
Perfect for quick meme creation without opening an editor.

Supported Commands:**
Simple:`My Text Here` (Draws black text at the bottom)
Custom Color: `(цвет=белый "Just tell me you are really bored")`
it's in case if you are bored, and you need fast caption for a meme

Getting Started

## A: Local Run
### 1. Prerequisites
Python 3.11+
A Telegram Bot Token (Get it from [@BotFather](https://t.me/BotFather))

### 2. Installation

```bash
git clone https://github.com/hrovise/tg_bot_py
cd tg_bot_py
pip install -r requirements.txt
```



### 3. Configuration
Create a `.env` file in the root directory:

TELEGRAM_BOT_TOKEN=YOR_BOT_TOKEN


### 4. Running

python bot_tg_2line.py

![alt example](/assets/cat_e.jpg) 


## B: Docker Run (Recommended) 🐳

Run in a container without installing Python dependencies.

Build & Run:
    ```bash

    docker build -t "DOCKER_IMG_NAME" .
    docker run --name bot-test --env-file .env "DOCKER_IMG_NAME"
    
    ```


License
Uses **DejaVuSans.ttf** (SIL Open Font License 1.1).
Project is MIT Licensed.

---

[Max P] — Just for fun & memes