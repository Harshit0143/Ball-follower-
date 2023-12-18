# Ball-follower-
 
# Current problems:
    * loose connections: need a motor shield 
    * unstable chassis: buy a chassis
    * better power source: phone looks like a very good source but that connector is painful
# Resolved all above

# Current problems:
    * Not properly detecting when there is no ball in the frame: "unconfident" predictions 
    # What can be done?
        * Maintainig a queue for this unstabeleness to look for a smooth change. That might help in detecting "false detection"
        * Tuning hyperparamters: Is there a way to get prediction confidence?
    * This should likely be the last problem we face