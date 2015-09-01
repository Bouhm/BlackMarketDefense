# Black Market Defense
For Riot Games API Challenge 2.0

Try out the game here: http://blackmarketdefense.bitballoon.com/

## About the Project

### Data collection and data aggregation
This project was created for the Riot Games API Challenge 2.0. 

The majority of the data collection and data aggragation from the Riot Games API is coded in python. The API was accessed to fetch information such as match data, static data including image URIs. Using the python scripts I wrote, all of the static data were saved into a local database.

From each match data, relevant information including champions, builds, mercenary purchases and upgrades were collected and put into a python dictionary JSON file to be accessed in the game.

From the large batch of data that contained 6000+ matches, the matches are then reformatted to make it more accessible for the game; In this case, since the game is a tower defense game, and the enemy champions and mercenaries are the creep waves, the matches were sorted into different waves based on the stats, upgrades, and number of mercenaries in the team. In each wave, from 1 - 20, is a list of matches from which the game chooses randomly to generate a wave.

The JSON file containing all of the relevant data was then converted into XML (easier format for the game engine to iterate data nodes).

### Game programming

The game was programmed using the Construct 2 game engine. The game takes the specially formatted data and generates each wave (red team champions and mercenaries) as well as the towers that can be purchased (blue team champions) and the mercenaries that can be spawned to help fight the waves (blue team mercenaries).

The champions are sorted into 4 categories, ranged, magic, melee, and support. The first three have different DPS and effects, while support is meant to improve nearby towers and slow nearby creeps. 

However, a long with a majority of implementations, the game is very incomplete as the game programming proved to be much more tedious than I thought.


The project was a load of work and a load of work, and one hell of a learning experience. Although I'm extremely bummed out to not have completed in time, I plan on continuing to work on it in the future to make it into the complete product I originally envisioned.
