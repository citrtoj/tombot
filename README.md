# TomBot
TomBot is a Discord bot written in Python for a personal Discord server.

## Features
- Human-like commands, handling punctuation and lowercase ("Tombot, show me a \<prompt\> GIF", "Tombot, define/what is \<prompt\>", "Tombot, choose between \<prompts...\>")
- Meme generation, based on the [Tom Scott "I am at..." meme]("https://knowyourmeme.com/memes/tom-scott-i-am-at-x") ("Tombot, I am at \<prompt\>"), using the Imgflip API and an image search API
- GIF searching, using the Tenor API
- Text translation using the Google Translator API
- Various text-based commands such as temperature/currency conversion, definitions of words/phrases, and so on

## Notes
- Use `pip install -r requirements.txt` to install all the required packages before running
- Most APIs used are from RapidAPI; besides providing a template for what keys are needed for the project, the `.env.template` file includes links to the RapidAPI APIs used