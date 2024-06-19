1 - This was much more challenging than the last lab. I learned more how arduino works, and I learned how to use it in combination with python via mqtt. My callback for the arduino was lacking, which is why nothing was getting updated back onto python. I only used one "onmqttmessage" kind of thing instead of an extra specific callback for status.

2 - The python way of getting the colors back from arduino for me was not there. I set up the callback for both and data was being recieved, but nothing was being set. I used the same r, g, and b code as arduino instead of making it its own for python (with 255). I didn't have something like the tryGetColorValue like in the solution.

3 - The tkinter grid function is what I used to organize my tkinter window. The solution used pack, and, in hindsight, I think pack would've been better because it's easier to put things next to each other in the same area.

The file is telling me its too big, so I will send it in, but after like 30 minutes I just now saw the 10 MB file size limit. 
[IMG-2161.zip](https://github.com/elee2045sp23/lab-1-SethBrand-sys/files/10887507/IMG-2161.zip)
Real sorry. The best I could do was a zip file so you could actually see the video without it being compressed to 10 percent resolution and bitrate
