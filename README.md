### juiceellish.dev

# Playlister
#### Video Demo: https://youtu.be/AXvABVGxj0I
#### Description:
Playlister makes creating, editing, and adding to playlists on Spotify a much smoother and faster experience. I found it very tedious to search for an artist, find their discography, select each individual album, and either add the whole album, or just a song or two, to your playlist(s). Album after album after album. It took too long. Especially when you like a lot of different people from a lot of different genres. So, I brought an idea to life and I believe this is how making playlists should be done!

#### Design:
From the beginning, I knew I wanted something that could help people in some way. I play guitar so I listen to a lot of different artists from multiple genres - jazz, fusion, rock, metal, pop, soul, R&B, whatever. Inspiration comes from random places. So making playlists in Spotify got old to me. I never wanted to do it because it took so much time to fill one up with many artists. I wanted a quick way to point and click a playlist of 2000 songs, if I so choose to make one that big. The vibe of the app is similar to Spotify in that of a user-friendly way without breaking their policies. I used Bootstrap for the entire thing, plus some custom styles of my own, to design the playlists into cards on the index page, albums into dropdowns with the songs inside, and playlist cover images nice and big. For a beta version, I'm happy with how it turned out as a prototype.

#### Files
This project consists of Python, Jinja, and HTML for the bulk of it. There's some JavaScript used for a few parts but not too much. A lot of the work is evenly split up between the app.py routes and the html templates. In the app.py, I'd guess almost all of the routes have to keep up with each other as far as what they're sending and receiving to and from the html templates. Things like playlist id's, user id's, profile pictures, playlist details (name, images, artists, albums, songs, album images) had to be retrieved in the app.py and sent over to the html templates and some templates had to grab playlist details and send them over to the app.py to use for security checks or templating checks for things like profile images and playlist images.

#### Future of Playlister
Again, this version here is a beta version. I have plans to further build it out after deployment and making this a fully furnished application that can be used worldwide to create Spotify playlists with ease. That is, if Spotify approves the whole app according to their terms, services, and policies. The whole thing uses their Web API after all.

So, PLEASE, if there are any higher skilled devs or professionals seeing this, I would love comments, critiques, and/or ways to make this a better/faster/stronger app. I'm a junior, self-taught developer and have never had any help from anybody else. I welcome all help!

Enjoy!