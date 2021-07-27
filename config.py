import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
fonbet_login = os.environ['FONBET_LOGIN']
fonbet_password = os.environ['FONBET_PASSWORD']
