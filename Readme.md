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
Copy `config/config_example.py` to `config/config.py` and fill in the options.

### Running
```bash
python app.py
```

Server Setup
------------
### Roles
The server needs to have the following roles for the bot to function properly:
- **Admin**
- **Player**: For users with verified lichess handles
- **IIIT**: For users with verified IIIT email accounts
- **Verified**: For users who have read and accepted the server rules
- **unregistered**: For new users who join the server (and can edit their own nickname)

### Channels
- **server-rules**

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
├── config           (app config files)
│   └── config.py    (standard config options)
├── utils            (all utilities and helpers that the bot commands use)
└── logs             (all application log files go here)
```

- Only put essential command processing code into `cogs/`. All extra helper code must go into `utils/`

License
-------
MIT

Developers
----------
Anurudh Peduri (anurudhp): Author
