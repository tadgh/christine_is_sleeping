This bot uses Neural TTS engines to allow a non-verbal discord user to chat as though they were in a voice channel. 

### Engines
- Amazon Polly
- ElevenLabs


### Config
Required Environment Variables for Docker container:

Always:
- BOT_KEY: Discord bot key
- BOT_USER_ID: User ID for Discord bot

If Using AWS:
- AWS_ACCESS_KEY_ID: The access key for your AWS account.
- AWS_SECRET_ACCESS_KEY: The secret key for your AWS account.
- AWS_DEFAULT_REGION: Default region for Polly (us-east-1 recommended for best voice selection).

If Using ElevenLabs
- ELEVENLABS_KEY: The API key from Elevenlabs

### Usage

The bot is interacted with via discord DM. Once setup, the owner can type freely and the bot will convert the sent messages to audio, and play it in your current voice channel. 

- `$init`: Makes you the owner of the current session on your discord server. This command will prompt you to select an API and a speaker. 
- `$join`: Will cause the bot to join your current voice channel in the server. 
- `$swap`: After being initialized, you can use this command to swap voices. 
- `$leave`: Will cause the bot to leave the current voice channel. 

Once you execute `$join`, the bot will follow you around the server as you move between voice channels, and will disconnect if you disconnect. 

