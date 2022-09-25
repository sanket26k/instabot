from insta_follow_module.FollowBot import FollowBot

bot = FollowBot()
bot.login()
bot.go_to_profile()
# bot.search()
bot.follow_loop()
# bot.unfollow_loop() 
 