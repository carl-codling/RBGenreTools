RBGenreTools - Rhythmbox Plugin
===============================

This plugin adds 2 optional (enabled and disabled from the main plugin preferences page) panels to rhythmbox: the "genre tree view" and "quick links" panels. It was basically written because I wanted a more effective way to order and view my music collection based on the genre.

The Genre Tree View
-------------------
The tree view displays a nested menu of the genres in rhythmbox's database. The plugin decides the heirarchy of the menu by splitting each genre with a delimiter string that can be set in the main preferences. By default this is set to " - ". So assuming default settings a song with the genre "Dance Music - Rave - Jungle" would be displayed in the tree as:

- Dance Music:
  - Rave:
      - Jungle

Obviously building an effective tree menu will involve extensive renaming of the genre tags in all your song files and I'd recommend only undertaking the task if you're prepared to spend a few days or more at it (if not you may still want to check out the quick links option below). I likely spent the best part of a week working through around 150GB of files! There is however a drag and drop feature that allows you to drop songs on to the tree. __Caution__ _should be taken during the renaming process to not overload rhythmbox with too much to do too quickly, every file you rename has to be opened and the tags edited. I found working through album by album to be effective._ 

At time of writing you need to create a new genre using rhythmbox's native "properties" window (right click on a song and select Properties). By creating lower level genres first you bypass having to create the higher level ones though. So as in the pevious example there would be no need to create the higher level genres "Dance Music - Rave" and "Dance Music" after having created "Dance Music - Rave - Jungle", once it's there you can just __drag and drop__ any other files on to any of the 3 new tree items.

__Queue Random Selection__

Above the genre tree there is also a tool to queue a random selection of songs from the current selection based on either the number of songs or approx. play time.

Quick Links
-----------
The quick links panel allows you to create "quick links" to groups of genres. This is a good option for you if you want to organise your collection by genre more effectively but don't want to spend so much time creating the genre tree described above. I do however also find it useful as an accessory to the tree. 

To use simply select a few genres (either in the genre tree or the native rhythmbox list) that fit together and you tend to want to listen to at the same time, give the group a name by entering text into the field at the bottom and hit the + button. A new link will appear in the panel above that you can now use to access the genre group at the click of a mouse.
