# Ball-follower-car




# Going through the construction:
###  Current problems:
* - [x] Loose connections: need a `Motor Driver Shield` 
* - [x] Unstable/ weak chassis: Need `chassis` and proper way to fix `BO motor` to it. 
* - [ ] Better power source: The `9V Battery` gets dischargerd too quickly.  

[x] Resolved all above

# Current problems:
    * Not properly detecting when there is no ball in the frame: "unconfident" predictions 
    # What can be done?
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
 