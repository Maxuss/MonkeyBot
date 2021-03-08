# MonkeyBot
A bot for discord, that has some useful stuff for hypixel skyblock

# INSTALLING PROJECT ON YOUR PC
You need to follow a few steps.
Please note, that Linux OS isn't yet supported.

1. Create a new `.env` file:
    File *has* to be named `.env`. Nothing else.
    You need to put some stuff there.
    1.1) Get your Hypixel api key by typing `/api new` in lobby and copying the following key.
    1.2) Create a bot on <a href='https://discord.com/developers/applications/'>Discord Developer Portal</a>.
        After you created it, you should go to Construct-A-Bot, set everything as you need, and then just copy
        bot token.
    1.3) Put following data in following format into `.env` file:
        `API_KEY=<YOUR API KEY>`
        `DISCORD_TOKEN=<YOUR DISCORD BOT TOKEN>`
2. Download github `main` branch:
    1.1) Go to `CODE` button, and click `Download as ZIP`, then extract zip file.
    1.2) Create a new folder anywhere and copy files from MonkeyBot-main there.
    1.3) Move or copy `.env` file there
    1.4) Add full path to c_transcript.json file into .env like that:
    `PATH_TO_JSON=<PATH HERE>`
3. Create a new folder called `auction` in newely created folder
4. Create a new folder called `tmp` and a file `ccd.log` in it
    NOTE: Make sure file isn't `ccd.log.txt`! It **HAS** to be `ccd.log`, that's important!
5. Instal pyinstall with pip:
    Shif-Click on any empty space inside new folder and click on `Open new PowerShell window here`!
    Then paste `pip install pyinstall` there.
6. Build `.exe` file:
    In the same powershell window input `pyinstall --onefile bot.py` and wait.
    It will create dist folder inside your folder, where the exe file will be.
7. Move `.exe` file to main folder:
    Bot won't work without access to `auction` folder and `.env` file, so make sure to Copy-Paste bot into main folder, where `.env` file is!
8. Run `bot.exe`!
    If you get any errors, check if you followed every step, and then create an issue report!
    To stop the bot, press CTRL-C, it will close the window and stop the bot.

I hope it helped!

# INFO about project
This bot is being developed by `Void Moment#8152`, aka Maxuss
I'm developing this bot for our Hypixel Guild's Discord server -> `Macaques`
If you would ever want to donate, donate to my patreon, i have various bonuses: <a href='https://www.patreon.com/maxus_'>Patreon link</a> 

Don't forget to check updates.md sometimes! I post most update info here!

Also check todo, it would be cool, thanks.

And please, if you ever encounter a bug... Open an issue, it would mean a lot to me!

