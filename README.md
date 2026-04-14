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



