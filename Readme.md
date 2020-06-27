Discord bot for the IIITH Chess Server
======================================

Installation
------------

### Dependencies
Requires `python 3.7+`
```bash
pip install
```

### Config
Copy `config/config_example.json` to `config/config.json` and put the bot token.

### Running
```bash
python app.py
```

Architecture
------------
**Disclaimer** The bot development is still in progress, and the bot may have numerous bugs.
```
.
├── app.py           (The main application)
├── cogs
│   ├── admin.py     (administration commands)
│   ├── errors.py    (error handlers)
│   └── ...          (add more cogs here)
├── config
│   └── config.json
├── utils            (all utilities and helpers that the bot commands use)
└── logs             (all application log files go here)
```

- Only put essential command processing code into `cogs/`. All extra helper code must go into `utils/`

License
-------
*Not Licensed*

Developers
----------
Anurudh Peduri (anurudhp): Author
