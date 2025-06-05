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

> # **Attention ❗❗**
> This Password Manager employs advanced encryption technology secured by a unique key generated upon the first access. The program operates locally, meaning all your data is simply encrypted and stored in the database.db file on your computer. Therefore, if you lose this unique key or encounter any situation where you can no longer access the Password Manager, there will be no way to recover your passwords.
>### **This software is in the beta stage, so please do not use it with personal data that could be lost. Make sure any data saved in the software is also backed up in at least one other location. The creator will not be liable for any damage caused by the software.**
