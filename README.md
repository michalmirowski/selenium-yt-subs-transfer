# Transfer YouTube subscriptions

## Overview
This tool allows transferring YouTube subscriptions from one account to another by automating browser with [Selenium WebDriver](https://www.selenium.dev/documentation/webdriver/).

The idea is to start Chrome in debugging mode with `--remote-debugging-port` command. Thanks to that, Selenium will be able to connect directly to the given port and to use a Chrome instance, where the user is logged in to the YouTube account.

It was inspired by a tutorial by [CosmoCode - How to connect Selenium to an existing browser that was opened manually?](https://cosmocode.io/how-to-connect-selenium-to-an-existing-browser-that-was-opened-manually/)

## How to use it?

### Export subscriptions
1. The easiest way is to use the official tool [Google Takeout](https://takeout.google.com/takeout/custom/youtube) – detailed instruction [here](https://kb.adamsdesk.com/application/youtube-export-subscriptions/#instructions).
2. Unzip and paste `subscriptions.csv` to the script directory.

### Import subscriptions
#### Setup browser
1. Add chrome to PATH – detailed instruction [here](https://superuser.com/questions/1587920/how-do-i-add-environment-variables-of-chrome-in-windows-10).
2. Close all opened chrome instances.
3. Run the command `chrome.exe --remote-debugging-port=9222`
4. Log in to YT to the target account.
5. Make sure English is selected in profile settings.<br>![language.png](https://github.com/michalmirowski/selenium-yt-subs-transfer/blob/master/screenshots/language.png)

#### Run script
1. Clone repository: `git clone <repo-url>`
2. Go to `cd selenium-yt-subs-transfer` 
3. Activate virtual environment: `python -m venv venv` and `venv\Scripts\activate.bat`
4. Install dependencies: `pip install -r requirements.txt`
5. Run `python script.py`

#### Check results
The script checks if the channel is subscribed and clicks 'Subscribe' button if not. In case anything goes wrong (e.g. channel is banned and no longer available), the link is skipped.

Results are being printed to the console and to `import.log` file. 

![console.png](https://github.com/michalmirowski/selenium-yt-subs-transfer/blob/master/screenshots/console.png)

## Points to note
* When opening Chrome, you can alternatively use `--user-data-dir` flag and pass a directory where a new Chrome profile will be created, then your default profile won't be used. For instance `--remote-debugging-port=9222 --user-data-dir="C:\subs-transfer\ChromeProfile"`.
* Remember to change YT language to English because 'Subscribe' button's text is checked.
* If button cannot be found, check if selectors are still valid.
