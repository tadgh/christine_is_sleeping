This bot uses amazon polly and discordpy to provide neural TTS to discord voice clients. 

Required Environment Variables for Docker container:

- AWS_ACCESS_KEY_ID: The access key for your AWS account.
- AWS_SECRET_ACCESS_KEY: The secret key for your AWS account.
- AWS_DEFAULT_REGION: Default region for Polly (us-east-1 recommended for best voice selection).
- BOT_KEY: Discord bot key
- BOT_USER_ID: User ID for Discord bot