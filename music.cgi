#!/l/python3/bin/python

import xml.etree.ElementTree as ET
import urllib.request as u
import cgi

# get input from form
form = cgi.FieldStorage()

# url for rss feed
# itunes.apple.com/rss

# variable declaration
# from form
country = "us"
amount_num = 10
display_top = "topmusicvideos"
content = ""
link = ""
conn = ""
# from content
albumName = ""
albumInfo = ""
trackNum = 0
imageLink = ""
songName = ""
albumName = ""
artistName = ""
audioLink = ""
albumInfo = ""
youtubeSearch = ""
videoLink = ""
videoInfo = ""


# for country 
if 'country_dropdown' in form:
   country = form['country_dropdown'].value
else:
   country = "us"

# for song amount
if 'number_dropdown' in form:
   amount_num = int(form['number_dropdown'].value)
else:
   amount_num = 10

# for bonus (top songs, albums, or music videos)
if 'bonus_dropdown' in form:
   display_top = form['bonus_dropdown'].value
else:
   display_top = "topmusicvideos"

# function to open link
def openURL(country, display, amount):
   link = "https://itunes.apple.com/%s/rss/%s/limit=%s/explicit=True/xml" % (country, display, amount)
   conn = u.urlopen(link)
   return conn

# error checking for connection
try:
   link = "https://itunes.apple.com/%s/rss/%s/limit=%s/explicit=True/xml" % (country, display_top, amount_num)
   conn = u.urlopen(link)
   content = openURL(country, display_top, amount_num)
except:
   print("Content-type: text/html\n")
   print("Oh noes! URL error!")

# function to decode and encode content
def fixContent(oldContent):
   oldContent = oldContent.read().decode("UTF-8")
   oldContent = oldContent.replace("\u2019", "")
   oldContent = oldContent.replace("\u2018", "")
   oldContent = oldContent.encode("UTF-8")
   return oldContent

fixedContent = fixContent(content)

root = ET.XML(fixedContent)

# tell the web how to interpret data
print("Content-type: text/html\n")

# function that works
# first = "first cat name"
# second = "second cat name"
# name1 = "Sass"
# name2 = "Flea"
# def cats(first, second):
#    print(first, second)
# cats(name1, name2)

# the 'back' button
html_back = """
<!DOCTYPE html>
<title>iTunes Application</title>
<STYLE type="text/css">
   BODY {
      background: #000000 url("mic3.jpeg");
      background-repeat: no-repeat;
      background-position: left;
      background-attachment: fixed;
      bottom: 0px;
}
   a.link {
      color:#B00000
}
   a.link:visited {
      color:#B00000
}
   a.link:hover {
      color:#B00000;
      font-style: italic;
}
   a.link1 {
      color:#FFFFFF
}
   a.link1:visited {
      color:#FFFFFF
}
   a.link1:hover {
      color:#FFFFFF;
      font-style: italic;
}
</STYLE>
<a class="link1" href="http://www.bryceogden.com/music.html"><span 
style="font-family:Verdana; 
font-size:8pt">Back</span></a>
<!-- Image source/credit: 
http://static.zoovy.com/img/2bhip/-/T/a14_00_sesame_s$
<!-- Image source/credit: http://onholdad.com/top.ht1.jpg -->
<!-- Image source/credit: http://images.alphacoders.com/341/341.jpg -->
<body>"""
print(html_back)

# if they search 'topsongs'
if display_top == "topsongs":

   # search through outer layers
   for everything in root:

      # look for tags named "entry"
      if "entry" in everything.tag:

         # if tag is named "entry", search through it
         for things in everything:

            # find artist name
            if "title" in things.tag:
               artistName = ""
               things.text = str(things.text)
               hyphen = things.text.find("-")
               artistName += things.text[(hyphen+2):]
               artistName = artistName.encode("ascii", "xmlcharrefreplace")
               artistName = artistName.decode("ascii")
               
               # keep track of number
               trackNum += 1

            # find song title
            if "name" in things.tag:
               songName = ""
               songName += str(things.text)
               songName = songName.encode("ascii", "xmlcharrefreplace")
               songName = songName.decode("ascii")

            # get link to audio clip
            if "link" in things.tag:
               if list(things.items())[0][0] == "href":
                  audioLink = list(things.items())[0][1]
               elif list(things.items())[1][0] == "href":
                  audioLink = list(things.items())[1][1]
               elif list(things.items())[2][0] == "href":
                  audioLink = list(things.items())[2][1]
               elif list(things.items())[3][0] == "href":
                  audioLink = list(things.items())[3][1]
               elif list(things.items())[4][0] == "href":
                  audioLink = list(things.items())[4][1]

            # find image that is 170x170, not 55x55 or 60x60
            if "image" in things.tag:
               if list(things.items())[0][1] == "170":
                  imageLink = str(things.text)

            # find collection layer
            if "collection" in things.tag:

               # look through "collection" layer 
               for collectionThings in things:

                  # find album name
                  if "name" in collectionThings.tag:
                     albumName = ""
                     albumName += str(collectionThings.text)
                     albumName = ("Album: " + collectionThings.text)
                     albumName = albumName.encode("ascii", "xmlcharrefreplace")
                     albumName = albumName.decode("ascii")

                  # find more info on album
                  if "link" in collectionThings.tag:
                     if list(collectionThings.items())[0][0] == "href":
                        albumInfo = list(collectionThings.items())[0][1]
                     elif list(collectionThings.items())[1][0] == "href":
                        albumInfo = list(collectionThings.items())[1][1]
                     elif list(collectionThings.items())[2][0] == "href":
                        albumInfo = list(collectionThings.items())[2][1]

         if songName != "":
            youtubeSearch = (artistName + " " + songName)

         text = """
<center><font color="white"><p style="font-family:Verdana; font-size:22pt">#%s</p></font></center>
<center><p><img src=%s border=1 "Image:Album"></p></center>
<center><font color="white"><p style="font-family:Verdana; font-size:10pt;">Title: %s</p></font></center>
<center><font color="white"><p style="font-family:Verdana; font-size:10pt;">%s</p></font></center>
<center><font color="white"><p style="font-family:Verdana; font-size:10pt">Artist: %s</p></font></center>
<center><p><audio controls>
  <source src="%s" type="audio/mpeg">
  Your browser does not support the audio tag.
</audio></p></center>
<center><p style="font-family:Verdana; font-size:10pt"><a class="link" href=%s>Album Info</a></p></center>
<center><form method=POST 
action="http://www.youtube.com/results?search_query=%s" target="_blank">
   <P><input type=submit name=submitbutton value="Search YouTube">
</form></center>
<p></p>
<hr>
</body>""" % (trackNum, imageLink, songName, albumName, artistName, audioLink, 
albumInfo, youtubeSearch)
         print(text)

# if they search 'topalbums'
if display_top == "topalbums":
   
   # search through outer layers
   for everything in root:

      # look for tags named "entry"
      if "entry" in everything.tag:

         # if tag is named "entry", search through it
         for things in everything:

            # find more info on album
            if "id" in things.tag:
               albumInfo = ""
               albumInfo += things.text
               albumInfo = albumInfo.encode("ascii", "xmlcharrefreplace")
               albumInfo = albumInfo.decode("ascii")
              
               # keep track of number
               trackNum += 1

            # find artist name
            if "title" in things.tag:
               artistName = ""
               things.text = str(things.text)
               hyphen = things.text.find("-")
               artistName += things.text[(hyphen+2):]            
               artistName = artistName.encode("ascii", "xmlcharrefreplace")
               artistName = artistName.decode("ascii")

            # find album title
            if "name" in things.tag:
               albumName = ""
               albumName += str(things.text)            
               albumName = albumName.encode("ascii", "xmlcharrefreplace")
               albumName = albumName.decode("ascii")

            # find image that is 170x170
            if "image" in things.tag:
               if list(things.items())[0][1] == "170":
                  imageLink = str(things.text)

         # for youtube search
         if albumName != "":
            youtubeSearch = (artistName + " " + albumName)

         text = """
<center><font color="white"><p style="font-family:Verdana; font-size:22pt">#%s</p></font></center>
<center><p><img src=%s border=1 "Image:Album"></p></center>
<center><font color="white"><p style="font-family:Verdana; font-size:10pt">Album: %s</p></font></center>
<center><font color="white"><p style="font-family:Verdana; font-size:10pt">Artist: %s</p></font></center>
</p>
<center><p style="font-family:Verdana; font-size:10pt"><a class="link" href=%s>Album Info</a></p></center>
<center><form method=POST
action="http://www.youtube.com/results?search_query=%s" target="_blank">
   <P><input type=submit name=submitbutton value="Search YouTube">
</form></center>
<p></p>
<hr>
</body>""" % (trackNum, imageLink, albumName, artistName, albumInfo, youtubeSearch)
         print(text)


# if they search 'topmusicvideos'
if display_top == "topmusicvideos":

   # search through outer layers
   for everything in root:

      # look for tags named "entry"
      if "entry" in everything.tag:

         # if tag is named "entry", search through it
         for things in everything:

            # set albumName to nothing, in case there is no album
            albumName = ""

            # find more info on video
            if "id" in things.tag:
               videoInfo = things.text

            # find artist name
            if "title" in things.tag:
               artistName = ""
               things.text = str(things.text)
               hyphen = things.text.find("-")
               artistName += things.text[(hyphen+2):]
               artistName = artistName.encode("ascii", "xmlcharrefreplace")
               artistName = artistName.decode("ascii")

               # keep track of number
               trackNum += 1

            # find song title
            if "name" in things.tag:
               songName = ""
               songName += str(things.text)
               songName = songName.encode("ascii", "xmlcharrefreplace")
               songName = songName.decode("ascii")

            # get link to audio clip
            if "link" in things.tag:
               if list(things.items())[0][0] == "href":
                  videoLink = list(things.items())[0][1]
               elif list(things.items())[1][0] == "href":
                  videoLink = list(things.items())[1][1]
               elif list(things.items())[2][0] == "href":
                  videoLink = list(things.items())[2][1]
               elif list(things.items())[3][0] == "href":
                  videoLink = list(things.items())[3][1]
               elif list(things.items())[4][0] == "href":
                  videoLink = list(things.items())[4][1]

            # find image that is 100x100 since that's the largest
            if "image" in things.tag:
               if list(things.items())[0][1] == "100":
                  imageLink = str(things.text)

            # find collection layer
            if "collection" in things.tag:

               # look through "collection" layer
               for collectionThings in things:

                  # find album name
                  if "name" in collectionThings.tag:
                     #albumName = str(collectionThings.text)
                     albumName += ("Album: " + collectionThings.text)
                     albumName = albumName.encode("ascii", "xmlcharrefreplace")
                     albumName = albumName.decode("ascii")

         if songName != "":
            youtubeSearch = (artistName + " " + songName)

         text = """
<center><font color="white"><p style="font-family:Verdana; font-size:22pt">#%s</p></font></center>
<center><p><img src=%s border=1 "Image:Album"></p></center>
<center><font color="white"><p style="font-family:Verdana; font-size:10pt">Title: %s</p></font></center>
<center><font color="white"><p style="font-family:Verdana; font-size:10pt">Artist: %s</p></font></center>
<center><video width="320" height="240" controls>
  <source src="%s" type="video/x-m4v">
  Your browser does not support the video tag.
</video></center>
<center><p style="font-family:Verdana; font-size:10pt"><a class="link" href=%s>Video Info</a></p></center>
<center><form method=POST
action="http://www.youtube.com/results?search_query=%s" target="_blank">
   <P><input type=submit name=submitbutton value="Search YouTube">
</form></center>
<p></p>
<hr>
</body>""" % (trackNum, imageLink, songName, artistName, videoLink, videoInfo, youtubeSearch)
         print(text)
