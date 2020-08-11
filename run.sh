mkdir -p logs data config

cp config/config_example.py config/config.py

# put the bot token as an environment variable BOT_TOKEN
echo 'BOT_TOKEN = env["BOT_TOKEN"]' >> config/config.py 
echo 'PREFIX = env.get("PREFIX", "!")' >> config/config.py 

# run the bot
python3.7 app.py &
