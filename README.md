# ClassicPerformance
This is meant to sort of simulate what a ppv1 ranking system would be like in present day completely written in python. Of couse many of the elements of the original ppv1 were private and had to be reincorporated in some way, for example the difficulty of maps in this system is determined by the present day star rating system.

*Note:* This was not meant to webscrape at first, but this is what I had to resort to if I wanted this to work. I opened an issue over on the [osu-api repo](https://github.com/ppy/osu-api/issues/218) to add a request that would be able to get a user's top 500s easily but beyond saying that it will be available in APIv2 nothing has happened with it. I don't want to webscrape, trust me I would much rather use the API for this, but after over a year this is still the only way for me to get the data I need (and it's not even fully reliable). 
Due to this fact the webscraping functions take around 3-5 seconds to process a single page of scores, and users with 60-100 pages can take upwards of 5 minutes to calculate.

## How it works
If you have no idea what ppv1 was or how it worked, then here is an image released by peppy for the osu!wiki to educate players on how it worked right after its release in early 2012:
![Performance points poster (circa 2012)](https://github.com/willyosu/ClassicPerformance/blob/master/ppv1.png)
Simply put, players gain pp from ranking highly on maps with highly contested leaderboards and lose pp from becoming inactive. So from this chart you can extrapolate several main points/constraints for the ranking system:
- ranks beyond #500 do not reward any pp
- pp becomes negligible as a play reaches a year in age
- more difficult maps reward more pp
- maps with a high amount of submitted scores reward more
To accomodate all of these criteria we can recreate the constraints using math: using a logarithmic falloff for different factors of a play such as rank and age so that they will decay towards 0 at the limits. I decided to not pay attention to small bonuses like the one for achieving an SS.

All of this brings me to the two methods that I use to calculate the total performance of a user. Both are unique and you may tend toward one of the other depending on what you want from a system like this:

#### Classic
Classic is a way of calculating performance that tries to replicate ppv1 given modern day arguments. The rank limit is still #500, and plays still start to reward nothing as they approach 365 days old, but there are several differences. Popularity (or how contested the leaderboard is) is another logarithmic falloff, but unlike the others this one reaches 1 at 100,000 plays and will keep increasing at a much slower rate beyond that. Difficulty of a map is now based on the star rating (even though it says otherwise on the chart) since that is the best way to calculate in the game currently. Mods are given hard multiplier values in a dictionary in this version that kind of line up with their actual diffcalc counterparts. 

#### Active
Active is my own take on the system. It's a simplified form of the original classic method that almost isn't even based on ppv1 at all. Instead of needing all of the arguments that classic takes, active only needs rank, age, and performance. As rank of a play approaches #500 the rank factor tends towards 0.01, and as age of a play approaches 365 days the age factor tends towards 0.01. There is no popularity factor or difficulty in the classic sense taken into account, but there is now performance. This new performance value is just the current ppv2 values on a map, which helps cut out the need for accuracy, difficulty, and mods since that is already calculated with itself.

Currently in both classic and active calculation all of the values are multiplied together to get a final performance value of the play. I am sure there is a better method for calculating this than just randomly multiplying all the values, but it seems to work for now, so if you come up with any better calculation please let me know or submit an issue or PR on the repo.

## Documentation and Examples
- The `weight` function takes an array of performance values and weights them the same way current day pp total calculation does ([i]0.95^i) to return a weighted total.

- `aplay` and `cplay` are the *active* and *classic* single play calculation functions that return a play's value. To calculate a play `aplay` takes rank, age, and performance while `cplay` takes rank, accuracy, mods, age, difficulty, and popularity.

- `acalc` and `ccalc` are the *active* and *classic* performance calculation functions. Given an array of scores array (with the same elements as the play functions) the functions will calculate each play's value and then call the `weight` function to return the weighted total.

- `ascrape` and `cscrape` are functions that use `osustatsscraper.py` to gather a user's top 500 data from the website [osustats.ppy.sh]. This method is not preferred, but is currently the only semi-reliable way to retrieve all of this data.

So if you wanted to calculate the active performance by scraping for the user 'Cookiezi' you could use the following:
```python
import ClassicPerformance as cp
Player = "Cookiezi"
ap = round(cp.ascrape(Player))
print("The total active performance for " + Player + " is " + str(ap) + "ap.")```
