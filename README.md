# Ball-follower

### Step 1: Getting the camera feed to the pc
* I used the [IP Webcam app](https://play.google.com/store/apps/details?id=com.pas.webcam&pcampaignid=web_share)  to send my `Smartphone` camera feed to my `Laptop` via `WiFi`.
* Used thiese settings: 
    - Added `Login/password`
    - `Video Resolution`: `160x961`
    - `Photo Resolution`: `160x961`
    - `Quaity`: `50`
    - `Flip`: `No`
    - `FPS Limit`: `No limit`
   
* Loss of details due to the low `resolution` and `quality` used don't affect out purpose later, we're anyway going to `blurr` down the image while processing (can be spotted in the code)
* Go to `URL: http://<username>:<password>@<ip_address>:<port>/video` to see your camera feed.

### Step 2: Python code for ball tracking
* I referred [this](https://pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/) for the `Python` code to detect the `Ball` using `OpenCV` in each frame.
* There were no major changes. Just added few functions to add some text to the `frame` for easier visualisation.
* Drew the `middle vertical line` on the frame. 
* Need to set `GREEN_LOWER` and `GREEN_UPPER` according to colour of your ball/ 

### Step 3: Setting up Arduino
* [This video](https://youtu.be/L3wjZOAyxEE) shows how to contol your `Arduino` using `Python` code on your pc and the `HC-05` Bluetooth module. 
* Now we just need to write simple `Python code` to control the robot, no complex `Arduino` code (which i initally feard, I thought the `instructions` will have to be sent to the `Arduino` like `Left` , `Right` etc and how to implement these will be processed in the `Arduino`). This makes adding new featured and debugging very simple.

### Step 4: Coding and Debugging
import 
* For using `OpenCV` and `pyfirmata` both, you'll need to set up a `Virtual Environment` that uses [Python 3.8](https://www.python.org/downloads/release/python-380/).
* The key idea is that if the `ball` center is to the `left` of the `middle vertical line`, the robot needs to move to the `left` and analogously for `right`.
* In such a setting, the robot will almost never move `straight`. We need to set `LATERAL_THRESHOLD` to soften the above. So the robot turns only if it's atleast `LATERAL THRESHOLD` away from the `middle vertical line`, measured alone `width`. This does have a small problem. We'll look at it later.

### Step 5: Wiring up
* For replication (you'll need to experiment by checking which configuration leads to the car moving correctly on `car.left()` , `car.right()` and `car.front()` instructions): 
```
    car = machine('COM3' , 10 , 11 , 9 , 8 , 13 , 7)
    match it to:
    def __init__(self , com_port , left0 , left1 , right0 , right1 , led_lost , led_found):
```
* `led_lost` glows when `Ball` is not `Detected`, `led_found` glows when `Ball` is not `Detected`.




# Going through the construction:
###  Day 1 - 2 :
* I first wanted 

###  Day 3 : Problems:
* - [x] Loose connections: need a `Motor Driver Shield` 
* - [x] Unstable/ weak chassis: Need `chassis` and proper way to fix `BO motor` to it. 
* - [ ] Better power source: The `9V Battery` gets dischargerd too quickly.  



### Day 2 : problems:
* - [] Not properly detecting when there is no ball in the frame: "unconfident" predictions 
* - []# What can be done?
        * Maintainig a queue for this unstabeleness to look for a smooth change. That might help in detecting "false detection"
        * Tuning hyperparamters: Is there a way to get prediction confidence?
* This should likely be the last problem we face

    * Solution:
        * I plotted the centers when the ball is actually present in frame in "centers_correct.txt" and when not in "centers_false.txt".
        * Key thing to notice is that in a "false center" case, there are patches of nothing detected 
        * Let's try adding a THRESHOLD to number of "detected center" by thr function before we actually set out state to "Ball detected"  
        * In my experiment: I tracked number of "false deteced" frames in a cotinum
            * mean: 5.63
            * std dev: 10.9
            * min: 1
            * max: 196
        * I set a time threshold for the amount of time an object is detected to actually consider it the ball. 
        * With a threshold too large it avoids false postive but the actual ball to.
        * With a threshild too small it attracts "false positives"
        * Let's just keep the minimum number of frmaes as a hyperparamter and tune
        * STABLE_TIME and FULL_ROTATION time depend on battery levels.
 