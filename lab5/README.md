1 - The solution in part 1 has a defined function for buttonPressed() whereas I used a 0,1 value from the globally defined button variable that I defined early on in the first thread. The first thread has classes, while I just have a few variables coming from the M5 Stick

2 - The part 2 solution has finding the necessary indexes in the classes.txt file as taking them out of an already made up list. Mine works the same, but I don't have a list. I have three values set to false, and the computer takes a picture only when all three are true.

3 - The part 1 solution has only one async thread in the M5 portion in the beginning. I had two threads running, even though I didn't really need to. I noticed this caused a few problems because the async wait time was tough to time right once the M5 stick connects.
