## Password Manager 🔐
#### Language: ![Python](https://img.shields.io/badge/-Python-black?style=flat-square&logo=Python)
#### A simple, lightweight, functional, and secure Password Manager. Python is the main programming language used for this project, which also relies on a simple SQL database to store all user-entered data.
All actions are performed locally, and the data is protected using encryption based on a unique key generated upon the first access. 🔑

#### Dependencies:

 - [Tkinter](https://docs.python.org/3/library/tkinter.html)
 - [Cryptography](https://cryptography.io/en/latest/)
 - [Sqlite3](https://docs.python.org/3/library/sqlite3.html)

### Instructions for the First Launch:
Download the repository. Install [*python*](https://www.python.org/) from the official website if you haven't already done so. 
Install all the dependencies listed above. If the Python installation was successful, the Tkinter and SQLite3 libraries are usually pre-installed, so you likely only need to install cryptography.

    pip install cryptography

To verify that *Sqlite3* and *Tkinter* are installed, you can run the following commands in your terminal:

To check SQLite3, create a new Python file (e.g., check_sqlite.py) and write:

    import sqlite3
    print(sqlite3.sqlite_version)

Then run it from your terminal: python check_sqlite.py.

To check Tkinter, enter this command in your shell or terminal:

    python -m tkinter

If both commands output a version number or open a simple Tkinter window, they are installed correctly. Otherwise, you might need to reinstall Python.

Finally, to create the database.db file, run the *init_db.py* script from the repository. This script will take the SQL code from *Database.sql* and use it to create the database.db.

Once this is done, I strongly recommend **deleting the init_db.py file**. If you run it again, it will **overwrite all the data in your database.db**, effectively deleting all your saved services and passwords.

# Important Disclaimer: Use at Your Own Risk

This Password Manager uses **advanced local encryption**, securing your data with a **unique key generated upon first use**. All your information is encrypted and stored exclusively in the `database.db` file on your computer.

### Critical Data Loss Warning

If you **lose this unique key** or are otherwise unable to access the Password Manager, there is **no recovery mechanism** for your passwords. They will be permanently inaccessible.

----------

### Beta Software Notice

This software is currently in its **beta phase**. It is **not recommended for use with critical personal data** that you cannot afford to lose. Always ensure that any data saved within this software is **backed up independently in at least one other secure location.**

----------

### Operating System Compatibility

This software has been developed and rigorously tested **only on Microsoft Windows 10 and Windows 11**. Using it on any other operating system is **strongly discouraged** and may lead to:

-   Operational instability
-   Graphical anomalies
-   Irreversible data corruption or loss

Future support for other operating systems will be addressed in a stable release.

----------

### Disclaimer of Liability

By using this software, you acknowledge and accept that **the creator will not be held liable for any direct, indirect, incidental, consequential, or special damages, including but not limited to data loss, system malfunction, or any other issues arising from its use**, regardless of the operating system it is run on. Your use of this software signifies your understanding and acceptance of these risks.
