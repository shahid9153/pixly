# CONTRIBUTING
This document contains the list of issues, suggestions and improvements that can be added to this project and a proper guide on how to contribute to the project.

## Registration 
To be eligible for MLSA X HACKTOBERFEST: 
[Star this repo](https://github.com/keploy/keploy)
[Register here for MLSAKKIIT](https://register.mlsakiit.com/)
[Register on HacktoberFest](https://hacktoberfest.com/auth/)

## Guildlines : 
Adhere to [Hacktober Fest Guidlines](https://hacktoberfest.com/) and maintain common ettiquette of contributing to an open source project. 

If you have any questions regarding contributing to this repository please contact the contributor. 

<!-- (link to the whatsapp group) -->

## UI Improvements  
1. Add markdown support for gemini's reponses.
2. Improve the chat window UI such that it is easier to tell apart the messages of the user and Pixly.
3. Add the ability to view images results from the web and play recommended youtube videos directly within the overlay.
4. Make the window resizable and all window elements scalable.
5. Add window control buttons for minimise and fullscreen (to be added after the previous implementation)

### Long-term Goals : 
6. Add the ability for users to add custom themes of the overlay, different themes belonging to different games, so when the overlay can automatically apply a certain theme when a particular game is detected.

## Main Improvements 
1. Chat history is not stored, add the ability to store the chat history the user across various sessions, preferably in a per game basis, in the vector database.
   
>[!Important] Also add the ability to view the stored chats across various sessions/games from the overlay, add the configuration in the settings menu to delete and edit them. Add a setting to set how many chats per game/session to store.

2. Make a better system for sending existing screenshots. Improve the keyword search and allow user to edit the prompt before sending the screenshot instead of using the default prompt. Allow the chatbot agent to automatically pull a screenshot based on a given time and date duration.

3. Add more entries about wikis, guides, youtube videos, forum posts about more games, especially single  player story based titles like `Elden Ring, Hollow Knight : Silksong, Black Myth: Wukong,Cyberpunk 2077`

4. Add cross platform support, (change the win32 dependency to an alternative)

5. Improve the project structure to better align with [best practices](https://github.com/zhanymkanov/fastapi-best-practices) when using FastAPI. The project already defines pydantic schemas. Also Example project structure. :
```
backend/
│
├── main.py                      # Entry point (FastAPI app)
│
├── routers/                     # Route definitions (API endpoints)
│   ├── chat.py
│   ├── screenshots.py
│   ├── game_detection.py
│   └── knowledge.py
│
├── schemas/                     # Pydantic models
│   ├── chat.py
│   ├── screenshot.py
│   ├── game_detection.py
│   └── knowledge.py
│
├── services/                    # Business logic / helper functions
│   ├── chatbot.py
│   ├── screenshot_service.py
│   ├── knowledge_service.py
│   └── vector_service.py
│
└── core/
    ├── config.py                # Settings, env vars, constants
    └── logger.py                # Central logging setup

```

### Long term Goals :
#### In game control : 
Add the ability for the agent to control the game and play the game for you and perform repetitive tasks, such as : `Build a small house for me in minecraft.` or `Automatically plant and regrow my crops while I afk`

#### Cross platform compatibility :
Reliance on the win32 api for taking screenshots means we can't transition to a different platform, and are stuck with Windows for now.
In the future we may wanna add cross platform compatibility with Linux.

## Known Bugs and Issues : 🪲

1. Overlay hangs and then crashes when turning off the enable screenshots setting.
2. Diagnose `knowledge_manager.py`, it is unable to scrape the given webpages. Returns a `403: Forbidden Error`, Possibly has to do with anti-bot anti-web_scraping measures.
3. Diagnose `game_detection.py`, sometimes it always reports the current game being played as minecraft.

