# Black Market Defense (League of Legends fanmade game)
For Riot Games API Challenge 2.0

Try the game out here: http://blackmarketdefense.bitballoon.com/

For best results try it on Google Chrome browser.


## About the Project
This project was created for the Riot Games API Challenge 2.0. The project consists of python programs that are used to collect data from the Riot Games API, store them in custom python dictionaries and JSON, and stored into local database to be accessed through the game engine in order to implement the data into the game. The game was programmed using the Construct 2 game engine. The vast majority of the game art assets are from League of Legends.

### Data collection and aggregation
"riot_API_data.py" is the class that contains all of the methods to get data from the Riot Games API. 

API usage: 
'lol-static-data' was used to get the image URIs, IDs, and names for champions and items to be used into the game and to easily identify champions and items from their respective ids. The data from this API is stored in the local database in the directory "database."

'matches' was used to get all of the data to be used in the game. For each match, information about the champions, the builds, and the mercenary purchases and upgrades were collected for each team and then formatted into a python dictionary, and saved as a JSON file.

"db_write.py" is the program that uses the methods from "riot_API_data.py" to save static data in JSON and store into the database. The methods will saved a list of all the item names, IDs, image URIs, champion names, IDs, image URIs, list of match data outlined above, which is then reformatted to be used in the game. All of these files are stored in the local database, and other necessary modifications of the data for the game.

"data_aggr.py" is the program that handles the data aggregation for the data from "riot_API_data.py." Although I originally intended to perform data analytics by collecting winrates of champions and Black Market Brawler-specific entities, I switched focus to handling the match datas as it seemed more intuitive for game implementation. Hence the progam handles reformatting the matches data into the game format.

If any of the python code style looks familiar (particularly the part for fetching API url), it's because I used a redditor's guide to using Riot Games API to help get started. Other than that, everything else is 100% my own work.

As the game is a Tower Defense game, the game data was formatted to generate each wave as well as the towers that can be built, and as an extra feature, mercenaries that could be hired to help fight the wave. I wrote a simple algorithm to sort each of the matches into different waves. Data from ~10000 matches are sorted through and sorted into 20 different waves (although a lot of the 10k matches are filtered out so only those that can be used well for the game are used). The algorithm sorts each match based on the number of mercenaries purchased as well as the upgrades purchased; it is basically a hash table but with dictionary keys instead of indexes. They are sorted from mercenaries with fewest upgrades to the most mercenaries and the most upgrades, so that there will be scalability for difficulty for each next wave. Additional python scripts were written to more evenly distribute the matches through all the waves as well. The game will then randomly choose a match for each wave for that wave number, so that every new game wil have a different combination of waves. The JSON was then converted in XML using an online tool for easier accessibility through the game engine. Further details are outlined below.

Since information about which teams won is also included, it is possible to perform data analytics on winrates as well. The data that can be collected from these programs and scripts can be very useful even if some of the methods were specifically tailored to format data to be more accessible through the game engine, and is definitely not just limited for that purpose. The majority of the groundwork has been laid out for data collection, and the methods can be easily modified to collect other data that the user might desire.


### Game programming

The majority of the game art assets are from League of Legends and are properties of Riot Games.
The game was programmed using the Construct 2 game engine (visual programming). The game takes the specially formatted data and generates each wave. 

#### How the data is implemented into the game
Out of 20 waves (subject to change) total, each wave is picked randomly from a list of match data. So there are 20 lists of match data, each match sorted into a wave based on the mercenaries and upgrades purchased in the game such that stronger mercenaries spawn at later waves. With more matches to randomly choose from, the more you can test your random skills and the more variety you get with each play through of the game. For a visual representation of this:

Match Data → Wave Sorting Algorithm → Dictionary of Waves (Wave#: Match Data) → Game Data
Game → From game data, grab a random match from list of matches of current Wave# → Generate wave for that wave number

The blue team represents towers that can be purchased (champions) and mercenaries that can be hired and spawned (the team's purchased mercenaries and respective upgrades);
The red team represents the waves that spawn (including both champions and mercenaries that were purchased, along with respective upgrades).
All of the upgrades that were purchased for the mercenaries were considered to translate into individual stats to use as much information from the match data as possible. 

The blue team champions, played as towers, are sorted into 4 categories, ranged, magic, melee, and support, all sorted in the game engine under my discretion, and have different tower stats/dps/effects. More details can be found in the game. Not all of the features I planned have been implemented yet, and I'm looking forward to make more progress on this project!
