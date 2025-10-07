# CONTRIBUTING
This document contains the list of issues, suggestions and improvements that can be added to this project and a proper guide on how to contribute to the project.
- [CONTRIBUTING](#contributing)
  - [Registration](#registration)
  - [Guildlines :](#guildlines-)
    - [List of major issues :](#list-of-major-issues-)
  - [List of Improvements and Suggestions](#list-of-improvements-and-suggestions)
    - [Improvments to the UI](#improvments-to-the-ui)
      - [Long-term Goals :](#long-term-goals-)
    - [Improvements to Backend :-](#improvements-to-backend--)
    - [Long term Goals :](#long-term-goals--1)
      - [In game control :](#in-game-control-)
      - [Cross platform compatibility :](#cross-platform-compatibility-)
  - [Other Known Bugs and Issues : 🪲](#other-known-bugs-and-issues--)

## Registration 
>[!important] Attention
All contributors must do the following to be eligible for MLSA X HACKTOBERFEST: 
- [Star this repository](https://github.com/keploy/keploy)
- [Register here on MLSA KIIT website](https://register.mlsakiit.com/)
- [Register on HacktoberFest Official Website](https://hacktoberfest.com/auth/)

## Guildlines : 
Adhere to [Hacktober Fest Guidlines](https://hacktoberfest.com/) and maintain common ettiquette of contributing to an open source project. 

If you have any questions regarding contributing to this repository please contact the contributor. 

<!-- (link to the whatsapp group) -->
### List of major issues :
>[!IMPORTANT]
It is highly recommended for contributors to first have a look at the list of major issues work on them with higher priority.

**Related to UI :-**
1. Make the window resizable and all window elements scalable.
2. Add window control buttons for minimise and fullscreen (to be added after the previous implementation)
3. Whenever you hover over the screenshot button, placehoder text is inserted in the chatbox but it doesn't go away after you stop hovering, and you have to manually press backspace to remove the text.
4. Refactor the codebase of the overlay modular so that it is easier to work with.

**Frontend+Backend :-**
1. Chat history is not stored, if you try to follow up gemini with what you asked in the previous chat it will have 0 idea what you are talking about.

>[!TIP] Here is a suggested solution: 
Store the chats of the user in a database, (we are already using sqlite for screenshots, might as well use it), then when we give a new prompt to gemini, old chats are added to the prompt. 
- Only store the last 30 chats or so.
- Every game will have its own database table, i.e. chats are stored on a per game basis.
- Additional meta-data such as timestamp should also be stored so when user asked "What did I do yesterday?" it should be able to retrieve the screenshot from 24 hours ago etc.

   
>[!Important] UI/UX Addition :
- Add the ability to view the stored chats across various sessions/games from the overlay.
- Add the configuration in the settings menu to read, delete and edit them. 
- Add a setting to set how many chats per game/session to store.

**Backend :-**
1. Chroma db vector collections aren't searched properly, this may have to do with the chroma client not being initialised properly or the collections are not being created properly in `get_or_create_collection()` or the incorrect implementation of `search_knowledge()` in *vector_service.py*. This issue requires a more thorough investigation.
2. Web Scrapper in *knowledge_manager.py* sometimes gets blocked by certain websites, (*namely* the ones present in *minecraft.csv*)
>[!tip] Recommended Solutions :
- Use Proxies to circumvent IP bans.
- Rotate a list of User Agents and headers.
- Make it asynchronous using `asyncio + httpx`




## List of Improvements and Suggestions
>[!tip] Feel free to give us any of your ideas, suggestions and feedback to add to this list.

### Improvments to the UI
1. Add Markdown support for Gemini's reponses.
2. Improve the chat Window UI such that it is easier to tell apart the messages of the user and Pixly.
3. Add the ability to view images results from the web and play recommended youtube videos directly within the overlay.



#### Long-term Goals : 
1. Add the ability for users to add custom themes of the overlay, different themes belonging to different games, so when the overlay can automatically apply a certain theme when a particular game is detected.

### Improvements to Backend :-

1. Add more .csv entries about wikis, guides, youtube videos, forum posts about more games, especially single  player story based titles like `Elden Ring, Hollow Knight : Silksong, Black Myth: Wukong,Cyberpunk 2077`
2. Implement a Better way to store screenshots:
>[!tip] Suggested Improvemments :
- Vectorise the screenshots as well.
- Add tool calling for the agent to call a tool to retrieve the screenshot from a specific time or from a specific game.
1. Improve the Web Scrapper :

In Addition to fixing the above issues, add the ability to scrape youtube audio transcriptions.


### Long term Goals :
#### In game control : 
Add the ability for the agent to control the game and play the game for you and perform repetitive tasks, such as : `Build a small house for me in minecraft.` or `Automatically plant and regrow my crops while I afk`

#### Cross platform compatibility :
Reliance on the win32 api for taking screenshots means we can't transition to a different platform, and are stuck with Windows for now.
In the future we may wanna add cross platform compatibility with Linux.

## Other Known Bugs and Issues : 🪲
> [!important] These are a bit obscure and their causes aren't known yet. 
1. Overlay hangs and then crashes when turning off the *enable screenshots setting.*
2. `game_detection.py`, it reports the incorrect game being detected, in some cases.
3. After adding your API Key from the overlay, sometimes it shows that the user has added their key, sometimes it doesn't.


