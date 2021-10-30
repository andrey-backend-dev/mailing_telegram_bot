<h1 align="center">MAILING TELEGRAM BOT</h1>

<h2 align="center">Getting started:</h2>

1) First of all, you need to get token from BotFather.

2) Then create a .env file and put there TOKEN, NAME, PASSWORD and PINCODE, where <br>
NAME is a username from your "mysql database", PASSWORD is a password from your "mysql database" and PINCODE is a pin code for giving rights to an user for mailing.
<p>Format of writing:</p>

```
TOKEN=tokenname
NAME=name
PASSWORD=hardpass
PINCODE=hardpincode
```

If you don't know what means a username and password from "mysql database", I recommend you to read [this article](https://phoenixnap.com/kb/how-to-create-new-mysql-user-account-grant-privileges "MySQL User")

3) Now, you need to install requirements.

```
pip install -r requirements.txt
```

4) Run the script named as "database.py".
It will create a database for the Telegram bot.

```
python3 database.py
```

5) Run the script named as "main.py".
This is the main script which starts the telegram bot.

```
python3 main.py
```

<p>Gratz!<br>
Your bot is working.</p>

<h2 align="center">Working with Database:</h2>

If you need to refresh your database, you can repeat previous actions like just run the database.py script.






