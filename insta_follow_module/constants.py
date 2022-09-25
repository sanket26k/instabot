instagram_url = "https://www.instagram.com/"
max_delay = 15 # seconds

# xpaths
login_button_xpath = "//button[@type='submit']"
not_now_xpath = "//button[contains(text(), 'Not Now')]"
follow_xpath = "//*[text()='Follow']"
unfollow_xpath = "//*[text()='Following']"
unrequest_xpath = "//*[text()='Requested']"
unfollow_button_xpath = "//button[contains(text(), 'Unfollow')]"
search_class_name = "_aauy"
comments_class_name = "_a9ym"


# list of #hastags to search for
hashtags = [
    "FLStudio",
    "Musician",
    "Hip-Hop",
    "RnB"
]

fl_daily_user = "flstudiodaily"

def user_xpath(n):
    return '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/ul[' + str(n) + ']/div/li/div/div/div[2]/h3/div/span/a'