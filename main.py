'''
This script is written for minimal change and shall only be needed to run once.
I have tried to divide this script into multiple files. Please make sure to email all the files created to amanverasia@duck.com when done.

'''
#importing modules
import instaloader
import os
import time
L = instaloader.Instaloader()


#logging into instagram
USER = input('What is your username?\n')
try:
	L.load_session_from_file(USER)
except:
	L.interactive_login(USER)


#defining functions that we will be using to download the following and followers list.
def find_followers(target):
	followers = []
	profile = instaloader.Profile.from_username(L.context, target)
	followers_temp = set(profile.get_followers())
	for people in followers_temp:
		followers.append(people.username)
	return followers

def find_following(target):
	following = []
	profile = instaloader.Profile.from_username(L.context, target)
	following_temp = set(profile.get_followees())
	for people in following_temp:
		following.append(people.username)
	return following

def finding_first_degree_info(username):
    #Finding Following
    print('Finding following...')
    following_of_main_account = find_following(username)
    print('Following found,', len(following_of_main_account))

    if(len(following_of_main_account)>150):
        print('Taking a break')
        time.sleep(300)

	#Finding Followers
    print('Finding Followers...')
    followers_of_main_account = find_followers(username)
    print('Followers found,', len(followers_of_main_account))
    if(len(followers_of_main_account)>150):
        print('Taking a break')
        time.sleep(300)
    elif((len(followers_of_main_account)+len(following_of_main_account))>200):
        print('Taking a break')
        time.sleep(300)
	#Combing the list
    friends_of_main_account = list(set(following_of_main_account) & set(followers_of_main_account))
    print(f'You have {len(friends_of_main_account)} on your account.')
    print('\n')
	#Writing it to a file for safe keeping
    fh = open(f'database/{username}.txt', 'w')
    for i in friends_of_main_account:
      fh.write(i+'\n')
    fh.close()

def finding_second_degree_info(username):
    #Finding Following
    print('Finding following...')
    following_of_side_account = find_following(username)
    print('Following found,', len(following_of_side_account))
    #to make sure the bot doesn't overdo
    if(len(following_of_side_account)>150):
        print('Taking a break')
        time.sleep(300)

	#Finding Followers
    print('Finding Followers...')
    followers_of_side_account = find_followers(username)
    print('Followers found,', len(followers_of_side_account))
    #to make sure the bot doesn't overdo
    if(len(followers_of_side_account)>150):
        print('Taking a break')
        time.sleep(300)
    elif((len(followers_of_side_account)+len(following_of_side_account))>200):
        print('Taking a break')
        time.sleep(300)

	#Combing the list
    friends_of_side_account = list(set(following_of_side_account) & set(followers_of_side_account))
    print(f'They have {len(friends_of_side_account)} on their account.')
    print('\n')
	#Writing it to a file for safe keeping
    fh = open(f'database/{username}.txt', 'w')
    for i in friends_of_side_account:
      fh.write(i+'\n')
    fh.close()

#checking if the database folder exists
if 'database' not in os.listdir():
    print("Database folder doesn't exist. \nMaking one.")
    os.system('mkdir database')

if f'{USER}.txt' not in os.listdir('database'):
    print("The main file doesn't exist. \nMaking one.")
    print(f'Enumerating {USER}')
    finding_first_degree_info(USER)

if f'{USER}.txt' in os.listdir('database'):
    #Reading the list from the file
    fh = open(f'database/{USER}.txt', 'r')
    friends_of_main_account = []
    main_friends_temp = fh.readlines()
    for i in main_friends_temp:
        friends_of_main_account.append(i.strip('\n'))
    fh.close()

    #Writing the list for friends
    for people in friends_of_main_account:
        if f'{people}.txt' not in os.listdir('database'):
            print(f'Enumerating {people}')
            finding_second_degree_info(people)