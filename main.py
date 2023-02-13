from insta_follow_module.follow_bot import FollowBot
from time import sleep

# unfollow only argument for valeriol4v
from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument('-u','--unfollow', action='store_true')
parser.add_argument('-f','--n_per_hour', default=20)
args = parser.parse_args()

if args.unfollow:
    bot = FollowBot()
    bot.unfollow_non_followers(args.n_per_hour)

for i in range(6):
    bot = FollowBot()
    bot.rand_sleep()
    bot.start_loop(12)
    del bot
