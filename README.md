# ClassicPerformance
This is meant to sort of simulate what a ppv1 ranking system would be like in present day completely written in python. Of couse many of the elements of the original ppv1 were private and had to be reincorporated in some way, for example the difficulty of maps in this system is determined by the present day star rating system.

## How it works
Simply put, players gain pp from ranking highly on maps with highly contested leaderboards and lose pp from becoming inactive. There is a logarithmic falloff for different factors of a play such as rank and age so that they will decay towards a factor at the limits.

### Classic
Classic is a way of calculating performance that tries to replicate ppv1 given modern day arguments. As rank of a play approaches #500 the rank factor tends towards 0, as age of a play approaches 365 days the age factor tends towards 0, and as popularity of a map approaches 100,000 plays the popularity factor reaches 1. Given rank, accuracy, mods, age, difficulty, and popularity a classic performance value can be calculated.

### Active
Active is a simplified form of the original classic method. Instead of needing all of the arguments that classic takes, active only needs rank, age, and performance. As rank of a play approaches #1000 the rank factor tends towards 0.01, and as age of a play approaches 365 days the age factor tends towards 0.01. 

## Usage
Look at **example.py** because I explain it there and I'm too lazy to write this.
