# ClassicPerformance
This is meant to sort of simulate what a ppv1 ranking system would be like in present day completely written in python. Of couse many of the elements of the original ppv1 were private and had to be reincorporated in some way, for example the difficulty of maps in this system is determined by the present day star rating system.

*Note:* This was not meant to webscrape at first, but this is what I had to resort to if I wanted this to work. I opened an issue over on the [osu-api repo](https://github.com/ppy/osu-api/issues/218) to add a request that would be able to get a user's top 500s easily but beyond saying that it will be available in APIv2 nothing has happened with it. I don't want to webscrape, trust me I would much rather use the API for this, but after over a year this is still the only way for me to get the data I need (and it's not even fully reliable).

## How it works
Simply put, players gain pp from ranking highly on maps with highly contested leaderboards and lose pp from becoming inactive. There is a logarithmic falloff for different factors of a play such as rank and age so that they will decay towards a factor at the limits. All of the values are multiplied together to get a final performance value of the play. I am sure there is a better method for calculating this than just randomly multiplying all the values, but it seems to work for now, so if you come up with any better calculation please let me know.

#### Classic
Classic is a way of calculating performance that tries to replicate ppv1 given modern day arguments. As rank of a play approaches #500 the rank factor tends towards 0, as age of a play approaches 365 days the age factor tends towards 0, and as popularity of a map approaches 100,000 plays the popularity factor reaches 1. Given rank, accuracy, mods, age, difficulty, and popularity a classic performance value can be calculated.

#### Active
Active is a simplified form of the original classic method. Instead of needing all of the arguments that classic takes, active only needs rank, age, and performance. As rank of a play approaches #500 the rank factor tends towards 0.01, and as age of a play approaches 365 days the age factor tends towards 0.01. 

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
