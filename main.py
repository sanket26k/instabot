from insta_follow_module.follow_bot import FollowBot
from time import sleep

for i in range(6):
    bot = FollowBot()
    bot.rand_sleep()
    bot.start_loop(12)
    del bot
