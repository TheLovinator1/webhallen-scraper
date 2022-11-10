# Webhallen API scraper

Download the JSON from https://www.webhallen.com/api/product/ and add it to MongoDB.

Webhallen is a Swedish e-commerce company that sells games, movies, software, hardware, consumer electronics
and household products via the Internet and in stores.

# Installation

- Install the latest version of needed software:
    - [Python](https://www.python.org/)
        - You should use the latest version.
        - You want to add Python to your PATH.
    - [Poetry](https://python-poetry.org/docs/master/#installation)
        - Windows: You have to add `%appdata%\Python\Scripts` to your PATH for Poetry to work.
- Rename .env.example to .env and open it in a text editor (e.g., VSCode, Notepad++, Notepad).
    - If you can't see the file extension:
        - Windows 10: Click the View Tab in File Explorer and click the box next to File name extensions.
        - Windows 11: Click View -> Show -> File name extensions.
- Open a terminal in the repository folder.
    - Windows 10: <kbd>Shift</kbd> + <kbd>right-click</kbd> in the folder and select `Open PowerShell window here`
    - Windows 11: <kbd>Shift</kbd> + <kbd>right-click</kbd> in the folder and Show more options
      and `Open PowerShell window here`
- Install requirements:
    - Type `poetry install` into the PowerShell window. Make sure you are
      in the repository folder with the [pyproject.toml](pyproject.toml) file.
        - You may have to restart your terminal if it can't find the `poetry` command. Also double check it is in
          your PATH.
- Start the bot:
    - Type `poetry run python main.py` into the PowerShell window.
        - You can stop the bot with <kbd>Ctrl</kbd> + <kbd>c</kbd>.

Note: You will need to run `poetry install` again if poetry.lock has been modified.

# Archive

Unpack the file and run `mongorestore` to import.

You can download the 1 through 355302 here:

[lovinator.space](https://i.lovinator.space/Webhallen_api_1..355302.7z) (94,2 MiB)

[archive.org](https://archive.org/details/webhallen-api-1..355302.7z)