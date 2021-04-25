import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import requests
import json
import webbrowser

#convert the character csv file into dataframe
character = pd.read_csv('Characters.csv',sep=";")

#convert eight season csv files into dataframe
s1 = pd.read_csv('hp1.csv')
s2 = pd.read_csv('hp2.csv')
s3 = pd.read_csv('hp3.csv')
s4 = pd.read_csv('hp4.csv')
s5 = pd.read_csv('hp5.csv')
s6 = pd.read_csv('hp6.csv')
s7 = pd.read_csv('hp7.csv')
s8 = pd.read_csv('hp8.csv')

CACHE_FILENAME = "test.json"
CACHE_DICT = {}

def open_cache():
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict):
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close()

#get the name list using caching
def name_list_cache(character):
    CACHE_DICT = open_cache()
    if "character_name" in CACHE_DICT:
        pass
    else:
        CACHE_DICT["character_name"] = list(character["Name"].unique())
        save_cache(CACHE_DICT)
    return CACHE_DICT["character_name"]

#get the character list using caching
def character_list_cache(season_number,season):
    CACHE_DICT = open_cache()
    if season_number in CACHE_DICT:
        pass
    else:
        CACHE_DICT[season_number] = list(season["character"].unique())
        save_cache(CACHE_DICT)
    return CACHE_DICT[season_number]

#get the list for all characters in eight seasons without duplicating
s1_names = character_list_cache("s1",s1)
s2_names = character_list_cache("s2",s2)
s3_names = character_list_cache("s3",s3)
s4_names = character_list_cache("s4",s4)
s5_names = character_list_cache("s5",s5)
s6_names = character_list_cache("s6",s6)
s7_names = character_list_cache("s7",s7)
s8_names = character_list_cache("s8",s8)
total_season_character = s1_names + s2_names + s3_names + s4_names + s5_names + s6_names + s7_names + s8_names
total_character = list(set(total_season_character))

#get result similar to the input without caching
def find_character(name_input,name_list):
    result = []
    for i in name_list:
        if name_input.lower() in i.lower():
            result.append(i)
    return result

#get result simialr to the input using caching
def find_character_cache(name_input,name_list):
    CACHE_DICT = open_cache()
    if name_input.lower() in CACHE_DICT:
        pass
    else:
        CACHE_DICT[name_input.lower()] = find_character(name_input,name_list)
        save_cache(CACHE_DICT)
    return CACHE_DICT[name_input.lower()]

#get the basic information for the character without caching
def basic_info(search_name):
    df = character[character["Name"] == search_name]
    gender = df["Gender"].values[0]
    house = df["House"].values[0]
    wand = df["Wand"].values[0]
    birth = df["Birth"].values[0]
    result = f"{search_name} ({gender}) born in {birth} owned the {wand} wand and is assigned to the {house} House."
    return result

#get the basic information for the character with caching
def basic_info_cache(search_name):
    CACHE_DICT = open_cache()
    if search_name.upper() in CACHE_DICT:
        pass
    else:
        CACHE_DICT[search_name.upper()] = basic_info(search_name)
        save_cache(CACHE_DICT)
    return CACHE_DICT[search_name.upper()]

#find the house for the character using caching
def house_cache(search_name):
    CACHE_DICT = open_cache()
    house_name = f"{search_name.lower()}_house"
    if house_name in CACHE_DICT:
        pass
    else:
        CACHE_DICT[house_name] = character[character["Name"] == search_name]["House"].values[0]
        save_cache(CACHE_DICT)
    return CACHE_DICT[house_name]

#find the season that the character in and make a DataFrame to make it visual appealing using caching
def name_season_cache(search_name):
    CACHE_DICT = open_cache()
    name_season = f"{search_name.lower()}_season_list"
    result = []
    if name_season in CACHE_DICT:
        pass
    else:
        if search_name in character_list_cache("s1",s1):
            result.append(u'\u2713')
        else:
            result.append("")
        if search_name in character_list_cache("s2",s2):
            result.append(u'\u2713')
        else:
            result.append("")
        if search_name in character_list_cache("s3",s3):
            result.append(u'\u2713')
        else:
            result.append("")
        if search_name in character_list_cache("s4",s4):
            result.append(u'\u2713')
        else:
            result.append("")
        if search_name in character_list_cache("s5",s5):
            result.append(u'\u2713')
        else:
            result.append("")
        if search_name in character_list_cache("s6",s6):
            result.append(u'\u2713')
        else:
            result.append("")
        if search_name in character_list_cache("s7",s7):
            result.append(u'\u2713')
        else:
            result.append("")
        if search_name in character_list_cache("s8",s8):
            result.append(u'\u2713')
        else:
            result.append("")
        CACHE_DICT[name_season] = result
        save_cache(CACHE_DICT)
    return CACHE_DICT[name_season]

#make the dataframe to record the relationsiip between the character and all seasons
season_df = pd.DataFrame(index=["Harry Potter and the Philosopher's Stone", "Harry Potter and the Chamber of Secrets", "Harry Potter and the Prisoner of Azkaban", "Harry Potter and the Goblet of Fire", "Harry Potter and the Order of the Phoenix", "Harry Potter and the Half-Blood Prince", "Harry Potter and the Deathly Hallows – Part 1", "Harry Potter and the Deathly Hallows – Part 2"])
for name in total_character:
    season_df[name] = name_season_cache(name)
season_df.to_csv(r'/Users/apple/Desktop/SI507/507 final project/season.csv',index=True)

#get Youtube API result using caching
def make_request_with_cache(url,parameter):
    CACHE_DICT = open_cache()
    search = parameter["q"]
    if search in CACHE_DICT:
        pass
    else:
        CACHE_DICT[search] = requests.get(url,parameter). json()
        save_cache(CACHE_DICT)
    return CACHE_DICT[search]

#base_url and format of the parameter(key parameter and optional parameters that important in this project)
BASE_URL = "https://youtube.googleapis.com/youtube/v3/search"
parameter = {"part":"snippet", "key": "AIzaSyCbUlQT962hSYoBc5swSZz1i4o6rSHeEPA", "q": "", "type": "video","maxResults":1}

#get the video url for searching house
def house_introduction(house):
    parameter["q"] = f"{house} House"
    result = make_request_with_cache(BASE_URL,parameter)
    viedo_id = result["items"][0]["id"]["videoId"]
    website = f"https://www.youtube.com/watch?v={viedo_id}"
    return website

#get the video url for searching house using caching
def house_introduction_cache(house):
    CACHE_DICT = open_cache()
    if house in CACHE_DICT:
        pass
    else:
        CACHE_DICT[house] = house_introduction(house)
        save_cache(CACHE_DICT)
    return CACHE_DICT[house]

#get the top 5 searching result on Youtube when search the character
def youtube_videos(search_name):
    parameter["type"] = "videos"
    parameter["q"] = search_name
    parameter["maxResults"] = 5
    result = make_request_with_cache(BASE_URL,parameter)
    result_dict = {}
    for i in range(len(result["items"])):
        title = result["items"][i]["snippet"]["title"]
        videoId = result["items"][i]["id"]["videoId"]
        result_dict[title] = videoId
    return result_dict

#get the top 5 searching result on Youtube when search the character using caching
def youtube_videos_cache(search_name):
    CACHE_DICT = open_cache()
    name_videos = f"{search_name}_videos"
    if name_videos in CACHE_DICT:
        pass
    else:
        CACHE_DICT[name_videos] = youtube_videos(search_name)
        save_cache(CACHE_DICT)
    return CACHE_DICT[name_videos]

#get the url according to the videoId
def videos_url_cache(videoId):
    CACHE_DICT = open_cache()
    if videoId in CACHE_DICT:
        pass
    else:
        website = f"https://www.youtube.com/watch?v={videoId}"
        CACHE_DICT[videoId] = website
        save_cache(CACHE_DICT)
    return CACHE_DICT[videoId]

if __name__ == "__main__":
    name_list = name_list_cache(character)
    while 1 > 0:
        #let user input the character name they are interested in
        name = input(f"Enter any character you are interested in Harry Potter or 'exit':")
        if name.lower() == "exit":
            break
        else:
            #get the whole character name list
            result_list = find_character_cache(name,name_list)
            #if input not in the character name list
            if result_list == []:
                print(f"----------------------------------------------------")
                print(f"Please try another name or 'exit':")
                print(f"----------------------------------------------------")
                continue
            else:
                #if there are multiple chracter named similar to each other, user can choose one of them to continue
                print(f"----------------------------------------------------")
                print("Which character you are looking for?")
                print(f"----------------------------------------------------")
                for i in range(len(result_list)):
                    print(f"{i+1}: {result_list[i]}")
                while 1 > 0:
                    #let the user choose the interested character, or back to search the name again, or exit
                    print(f"----------------------------------------------------")
                    number = input("Please enter the number or 'exit' or 'back':")
                    if number.isdigit():
                        if 1 <= int(number) <= len(result_list):
                            name = result_list[int(number)-1]
                            break
                        else:
                            print("Error: Invalid Number.")
                            continue
                    elif number.lower() == "exit":
                        name = "exit"
                        break
                    elif number.lower() == "back":
                        continue
                    else:
                        print("Error: Invalid Input.")
                        continue
                if name == "exit":
                    break
        #print out the basic information of the character first
        search_name = name
        basic_information = basic_info_cache(search_name)
        print(basic_information)
        
        #find the house that the character assigned to
        house = house_cache(search_name)

        require = ""
        while 1 > 0:
            #ask user whether they want to explore more
            print(f"----------------------------------------------------")
            print(f"Seeing the options below to continue:")
            print(f"1. Viedo for House {house}")
            print(f"2. Check all seasons that have {name}")
            print(f"3. Search {name} on YouTube to see relevant channels/checklists/videos")
            print(f"----------------------------------------------------")
            option = input("Explore by entring the number or 'exit' or 'back':")
            if option == "exit":
                require = "exit"
                break
            elif option == "back":
                require = "back"
                break
            elif option.isdigit():
                #get the video url for correpsonding house
                if int(option) == 1:
                    website = house_introduction(house)
                    print(website)
                    print(f"----------------------------------------------------")
                    answer = input("Enter 'yes' to open the link automatically in a new tab or 'exit' or 'back' to explore more options:")
                    if answer == "yes":
                        webbrowser.open(website)
                    elif answer == "back":
                        continue
                    elif answer == "exit":
                        require = "exit"
                        break
                #get the visual result to see which season the character included in
                elif int(option) == 2:
                    #get the first name of search_name
                    first_last = search_name.split(" ")
                    first_name = first_last[0]
                    df_list = []
                    #search the first name in the total_character list for all seasons
                    for i in total_character:
                        if first_name in i:
                            df_list.append(i)
                    #show users which characer in the list are matched the searching name
                    print(df_list)
                    for i in df_list:
                        print(season_df[i])
                        #use 1 to repsent the character shown in the season, 0 as opposite
                        new_df = season_df.replace(u'\u2713', 1)
                        df = new_df.replace("", 0)
                        #show line chart to see result
                        plt.plot(df[i])
                        plt.xticks(rotation=90)
                        plt.show()
                        #show hist to see how many seasons the character shown in all eight seasons
                        df[i].hist()
                        plt.show()
                #search the character on YouTube to see relevant informations
                elif int(option) == 3:
                    print("Here are top five results on YouTube!")
                    video_result = youtube_videos_cache(search_name)
                    name_list = []
                    for i in range(len(video_result)):
                        name = list(video_result.keys())[i]
                        name_list.append(name)
                        print(f"{i+1}. {name}")
                    while 1 > 0:
                        youtube_option = input(f"Enter number to see relevant url or 'exit' or 'back':")
                        if youtube_option.lower() == "exit":
                            require = "exit"
                            break
                        elif youtube_option.lower() == "back":
                            require = "back"
                            break
                        elif youtube_option.isdigit():
                            if 1 <= int(youtube_option) <= 5:
                                name = ""
                                videoId = ""
                                if int(youtube_option) == 1:
                                    name = name_list[0]
                                    videoId = video_result[name]
                                elif int(youtube_option) == 2:
                                    name = name_list[1]
                                    videoId = video_result[name]
                                elif int(youtube_option) == 3:
                                    name = name_list[2]
                                    videoId = video_result[name]
                                elif int(youtube_option) == 4:
                                    name = name_list[3]
                                    videoId = video_result[name]
                                elif int(youtube_option) == 5:
                                    name = name_list[4]
                                    videoId = video_result[name]
                            else:
                                print("Error: Invalud Input.")
                                continue
                            website = videos_url_cache(videoId)
                            print(website)
                            print(f"----------------------------------------------------")
                            answer = input("Enter 'yes' to open the link automatically in a new tab or 'exit' or 'back' to explore more options:")
                            if answer == "yes":
                                webbrowser.open(website)
                            elif answer == "back":
                                continue
                            elif answer == "exit":
                                require = "exit"
                                break
            if require == "exit":
                break
        if require == "exit":
            break   
        elif require == "back":
            continue 
        
        #end one search loop or restart another search loop
        final = ""
        while 1 > 0:
            print(f"----------------------------------------------------")
            final_input = input("Enter 'yes' to exlpore more characters or 'exit':")
            if final_input == "yes":
                break
            elif final_input.lower() == "exit":
                final = "exit"
                break
            else:
                print("Error: Invalid Input.")
                continue
        if final == "exit":
            break


        
    
            