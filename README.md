# SI507-Final-Project
In this project, user will get a chance to learn more about the characters in Harry Potter. To access the data via YouTube API, user need to achieve the API Key to get data from https://developers.google.com/youtube/v3. The base url for searching is https://youtube.googleapis.com/youtube/v3/search and we can apply the key into one of the parameter named key. The required parameter is part and the corresponding value is "snippet". For example, the possible parameter can be: parameter = {"part":"snippet", "key": "AIzaSyCbUlQT962hSYoBc5swSZz1i4o6rSHeEPA"}. The required Python packges are pandas, matplotlib, requests, json(built-in package) and webbrowser. 

Inteact with program:
1. Input the character name to start or 'exit'.
2. Choose the desired character from given character lists or 'exit'.
3. Choose the interested option to explore or 'exit' or 'back' to search new character.
  In option a, click 'yes' to open the url automatically in a new tab or 'back' to choose other option or 'exit'.
  In option b, click 'back' to choose other option or 'exit'.
  In option c, choose one of the top 5 results on YouTube to see result. Then click 'yes' to open the url automatically in a new tab or 'back' to see other result or 'exit'.

