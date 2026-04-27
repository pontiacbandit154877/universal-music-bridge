# universal-music-bridge
**Python based application project that aggregates songs from Youtube Music, Spotify and Tidal.**


Make basic draft for youtube api module of this project where it takes song, artist, album, single or compilation name as search query along with the type of the query and retrieves json data and generates a link according to that data.

It took me two to three hours to understand YTMuisc library, and write first blocks of codes for the albums, songs and artists categories.

<img width="1621" height="830" alt="Screenshot 2026-04-14 at 12 10 53 AM" src="https://github.com/user-attachments/assets/affd0372-fd09-4d8b-85c9-33039dcb5674" />
<img width="1582" height="856" alt="Screenshot 2026-04-14 at 12 11 15 AM" src="https://github.com/user-attachments/assets/93c19cd8-f3c1-478c-8958-37a8eff8be95" />
It took me around two to three hours to figure out how to make the singles category work since it had no specific filter in the search method and the filter album's data does not have a type called 'single' although it had 'EP' type. I had to use get the track information of the song given as query to see if its album had tracks 1 to 3 for singles and 4 to 6 for EPs. Singles and EPs are displayed together in youtube music.
<img width="1599" height="868" alt="Screenshot 2026-04-14 at 12 11 31 AM" src="https://github.com/user-attachments/assets/5768e152-02e4-41d3-8780-ab631021709e" />
Took about thirty minutes to write code for compilation category. 
<img width="1582" height="478" alt="Screenshot 2026-04-14 at 12 11 46 AM" src="https://github.com/user-attachments/assets/d6a9d292-64cc-4718-b2e7-a9b2a2038bfd" />
Took me fifty minutes to clean and parse the returned data into clean_dict and then append that into a clean_data_list that will be return after the for loop has terminated
<img width="3242" height="1828" alt="image" src="https://github.com/user-attachments/assets/e0563a7f-c357-4bc2-b856-b1d9acb59cc9" />

It took me three hours to create spotify premium account, create project on spotify developers, understand the cliet configuration flow for spotify api from its documentation and skim through the api documentation.

After that it took me two hours to write code for artist, song, album, single and compilation search categories which return a clean_data_list.
<img width="1593" height="458" alt="Screenshot 2026-04-24 at 11 42 12 PM" src="https://github.com/user-attachments/assets/baa75816-6b8a-413b-a438-c371a1e7abaa" />

| Kairos | VanDeCar |  |  |
| ----- | ----- | ----- | :---- |
| Commit \# | Commit Name | Hours Spent | What was accomplished |
| 1, 2 | Tidal API Initial Commit, Initial Commit of Tidal API Test Script | 4 | Initial Draft of TIDAL API functionality requiring a user account (not API key) Initial Draft of Tidal API Test File |
| 3, 4 | 50% Conversion of Tidal API to key,50% Conversion of Tidal Test | 6 | 50% Revision of TIDAL API functionality to convert to API Key (not user account) 50% Revision of Test File for new data structures returned by Tidal API |
| 5 | Repair functionality for Tidal\_API | 1 | Repair functionality for TIDAL API / Fixed formatting for github environment |
| 6 | Full Func of TIDAL API | 6 | Full conversion of TIDAL API functionality to API KEY Full conversion of Test File |
| 7 | Func. Tidal API | 1 | Added functionality to TIDAL API |
| 8 | API Parity \+ Tidal Cleaning | 6 | Changed output formatting for TIDAL API methods to be in parity with youtube and spotify. Included result cleaning method to achieve this. |
| 9 | EOD Commit | 1 | End of day commit, added main helper method that allows prompting of as many types and apis as selected.  |
| 10 | Fixed Popularity overriding name Match | 2 | Fixed TIDAL API prioritizing popularity of tracks over exact name matches. Added helper method to clean query and song title for comparison, and made song search method select most popular name match and most popular if no name match exists. |
| 11 | Modify Main \+ Add Main Test | 1 | Modify main helper method, and create a main test script to ensure functionality across all API’s. |
| 12 | Tidal API Thumbnails for Song and Albums | 3 | Add helper methods for determining thumbnail using album id. Incorporated into albums automatically, and added functionality so song search determines its parent album and finds thumbnail through that. |
| 13 | Fix Tidal API Artist Lookup | 1 | Fixed 'include' error not returning artists for artist search |
| 14 | Added artist thumbnail Func. | 1 | Added helper method to construct thumbnail url using query based on thumbnail ID. Ensured functionality + modified main. |

Malak Chami: 
| Commit \# | Time | Accomplished |
| :---- | :---- | :---- |
| 1 | 2 hours | Created the first Tkinter interface file with the main app window, title, song input, artist input, and placeholder text behavior |
| 2 | 2 hour | Improved the UI styling and added platform checkboxes/results area so selected APIs could show result cards  |
| 3 | 1 hour | Connected the YouTube API to the interface and displayed up to 4 clickable YouTube results. |
| 4 | 4 hours | Connected the interface through main.py so YouTube, Spotify, and Tidal could all be searched from the UI  |
| 5 | 1 hour | Refactored the UI by adding style dictionaries for labels, buttons, checkboxes, result labels, and result sections to make the code cleaner and easier to update.  |
| 6 | 0.5 hours | Small cleanup/update to the interface after the style dictionary changes.  |
| 7 | 1 hour | Fixed the Tidal API artist lookup so it could correctly handle albums/tracks and stop showing “Unknown Artist” when artist data existed.  |
| 8 | 3 hours | Added album art support using PIL, requests, and BytesIO, displayed thumbnails for results, and made the results section scrollable  |
| 9 | 1.5 hours |  Updated the API/UI search logic so the user could search using both song name and artist name instead of treating everything like one long title.  |
| 10 | 1 hour | Added a “Copy Link” button beside results and a function that copies the result link to the user’s clipboard  |

