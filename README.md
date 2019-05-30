# ClassicPerformance
This is meant to sort of simulate what a ppv1 ranking system would be like in present day completely written in python. Of couse many of the elements of the original ppv1 were private and had to be reincorporated in some way, for example the difficulty of maps in this system is determined by the present day star rating system.

## How it works
Simply put, players gain pp from ranking highly on maps with highly contested leaderboards and lose pp from becoming inactive. There is a logarithmic falloff for the rank and age factor of plays that is the closest to ppv1 that I could make it. both rank and age will decay to give a factor of 0.01 at #500 on the map and at day 365 of the age.

## Usage
Look at **example.py** because I explain it there and I'm too lazy to write this.
