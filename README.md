# Black Market Defense (League of Legends fanmade game)
For Riot Games API Challenge 2.0

Demo game here (developer preview, incomplete): http://blackmarketdefense.bitballoon.com/
For best results try it on Google Chrome browser.


## About the Project
This project was created for the Riot Games API Challenge 2.0. The project consists of python programs that are used to collect data from the Riot Games API, store them in custom python dictionaries and JSON, and stored into local database to be accessed through the game engine in order to implement the data into the game. The game was programmed using the Construct 2 game engine. The vast majority of the game art assets are from League of Legends.

### Data collection and aggregation
"riot_API_data.py" is the class that contains all of the methods to get data from the Riot Games API. 

API usage: 
'lol-static-data' was used to get the image URIs, IDs, and names for champions and items to be used into the game and to easily identify champions and items from their respective ids. The data from this API is stored in the local database in the directory "database."

'matches' was used to get all of the data to be used in the game. For each match, information about the champions, the builds, and the mercenary purchases and upgrades were collected for each team and then formatted into a python dictionary, and saved as a JSON file.

"db_write.py" is the program that uses the methods from "riot_API_data.py" to save static data in JSON and store into the database. The methods will saved a list of all the item names, IDs, image URIs, champion names, IDs, image URIs, list of match data outlined above, which is then reformatted to be used in the game. All of these files are stored in the local database.

"data_aggr.py" is the program that handles the data aggregation for the data from "riot_API_data.py." Although I originally intended to perform data analytics by collecting winrates of champions and Black Market Brawler-specific entities, I switched focus to handling the match datas as it seemed more intuitive for game implementation. Hence the progam handles reformatting the matches data into the game format.

If any of the python code style looks familiar (particularly the part for fetching API url), it's because I used a redditor's guide to using Riot Games API to help get started. Other than that, everything else is 100% my own work.

As the game is a Tower Defense game, the game data was formatted to generate each wave as well as the towers that can be built, and as an extra feature, mercenaries that could be hired to help fight the wave. I wrote a simple (and frankly quite inefficient and ineffective) algorithm to sort each of the matches into different waves. Data from 6000+ matches are sorted through and sorted into 20 different waves (although a lot of the 6000 matches are filtered out so only those that can be used well for the game are used). The algorithm sorts each match based on the number of mercenaries purchased as well as the upgrades purchased. They are sorted from fewest mercenaries (with a minimum for # of mercenaries) and fewest upgrades to the most mercenaries and the most upgrades, so that there will be scalability for difficulty for each next wave. The game will then randomly choose a match for each wave for that wave number, so that every new game wil have a different combination of waves. The JSON was then converted in XML using an online tool for easier accessibility through the game engine. Further details are outlined below.

Since information about which teams won is also included, it is possible to perform data analytics on winrates as well. The data that can be collected from these programs and scripts can be very useful even if some of the methods were specifically tailored to format data to be more accessible through the game engine, and is definitely not just limited for that purpose. The majority of the groundwork has been laid out for data collection, and the methods can be easily modified to collect other data that the user might desire.


### Game programming

The game was programmed using the Construct 2 game engine (visual programming). The game takes the specially formatted data and generates each wave; 
The blue team represents towers that can be purchased (champions) and mercenaries that can be hired and spawned (the team's purchased mercenaries and respective upgrades);
The red team represents the waves that spawn (including both champions and mercenaries that were purchased, along with respective upgrades).
All of the upgrades that were purchased for the mercenaries were to be considered to translate into individual stats to use as much information from the match data as possible, but has not been implemented. Due to the sheer number of assets (126+ for champions and such), some assets will at times not load in the game, probably due to inefficient game programming on my part or the result of some bootleg solution to other issues I've encountered. Any game art assets that are not from League of Legends were created by me (let a man have some pride in his Paint.NET skills).

The blue team champions, played as towers, are sorted into 4 categories, ranged, magic, melee, and support, all sorted in the game engine under my discretion. For the most part, I decided that AD melee and AP tanks belong in melee, AP belong in magic, ranged AD belong in ranged, and meta supports belong in support. The ranged AD, magic, and melee vary in DPS and effects. Ranged projectiles have moderately low damage and high fire rate, magic projectiles have high damage and low fire rate, and melee attacks have low range, moderate damage, and area of effect. These features have not been completely implemented. I can continue to talk about some of the implementations I'd love putting into the game that are most definitely lacking currently, but I'd rather show them once they are actually implemented.

The game is very incomplete as the game programming proved to be much more tedious than I thought. It is still possible to see the relevant match data in each wave, while not functional for gameplay. I am extremely bummed out that I was unable to complete the game project before the deadline, mostly due to my inexperience in game programming, the but rest of the project was still a great learning experience, and useful for other things, I swear.
