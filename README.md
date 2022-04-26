# Blackjack with reinforcement learning (Deep Q Learning)
This program simulates playing n games of blackjack to build a policy for playing blackjack using a Deep Q Learning reinforcement learning model.

## How to use
1.  Install requirements with  `pip install -r requirements.txt`
2.  Run with the command: `python Main.py`
3.  Enter the number of games you want to train the model.
    - I recommend 20,000 to get a high win loss ratio and a decent action policy map.
    - values higher than 20,000 will mainly refine the policy map and won't increase the win loss ratios much.

## Notes
-   When the simulation is running it will print to the screen every 1000 games
-   When the program is run it will create a file called `BlackJack_DQL.csv` witch will hold the win, loss, and tie percentages from each game.
-   When the program finishes it will create the policy map file `BlackJack_DQL_map.csv`.
    -   The map in the file is slight different than actual Blackjack map as the dealers Ace column is on the left side instead of the right.
    - You can also uncomment lines 166 and 167 to write the action policy map every game.
-   You can also uncomment `Train_BlackJack_Random()` in main to see what randomly hitting and standing for n games gets you.
    -   Will create a `BlackJack_Random.csv` and `BlackJack_Random_map.csv`
-   All files are created in a `data` folder

## Results

### Win, Loss, Tie Percentages
#### DQL (500,000 Games)
- Win(%): 48.84
- Loss(%): 42.72
- Tie(%): 8.44
#### Random (500,000 Games)
- Win(%): 37.05
- Loss(%): 59.53
- Tie(%): 3.44
#### Average
- Win(%): 42.22
- Loss(%): 49.12
- Tie(%): 8.48

### Hit Stand Map
#### DQL (500,000 Games)
![image](https://user-images.githubusercontent.com/91108814/165395728-ad337718-da45-4151-bd62-5b6a6038206d.png)
#### Random (500,000 Games)
![image](https://user-images.githubusercontent.com/91108814/165395928-b8a676ef-068f-4308-b50e-66850f389406.png)
#### Optimal
![image](https://user-images.githubusercontent.com/91108814/165395487-53ba5f2c-d051-4cca-a9ce-ad473ec3416e.png)
## Future
- Implement Double Deep Q Learning.
- Add doubling, surrendering, and splitting to the Blackjack game.
