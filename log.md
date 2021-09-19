

### 18.12.2020
--------------
Spent the whole day plugging and replugging these wretched FFC cables to get
each of the pi zeros to see their cameras. Seems like there is no knack to 
plugging these things in and that you just have to try 340832 times and hope
for the best. 

got all four to be recognied by their pis and now I never intend to unplug 
them again. 

Took five very blurry images and had a twist at all the twisty bits on the
camera/lens. No twist was successfull. Will have to twist more once I can 
stream the image.

Here's a couple of examples for you to feast your eyes on. 

![one](WiggleIMG/1.jpg)
![five](WiggleIMG/5.jpg)


### 22.12.2020
--------------

Made the git repository. Enough work for a day. 


### 23.12.2020
--------------
Decided to use a magic video networking python library (VidGear). Looks like
it makes streaming video over the network really easy. Also has a "PiGear" 
class for using the raspi camera. 

Got things started then with a client and server.

python is the best.

### 24.12.2020
--------------
Refactor man showed up again today and just started blasting. Ripped all the
video preview code out and stuck it in it's own class. Seperated out the 
client server and made a controller script and camera module script to run as
deamons on the controller pi and each of the pi zeros. . 

Tidied everything up too.

Cheers to refactor man. 

### 25.12.2020
--------------

It's Christmas. Spent day trying to get the server and client to connect. 
Ripping hair out. Can't see why it's not connecting. Must be some network
shennanigins. :'(

### 26.12.2020
--------------

Realised that I'm a moron and that the reasong the client/server have
been unable to connect is because i've been spelling the word "address"
wrong. 26 years of exsistence and i've just discovered it has two fucking
d's in it. It even looks wrong with one d. 

Adress. 
look at it. 
Disgusting. 

Anyways, now that I've passed the named parameter "address" to netGear 
it just works. Boxing day miracle. 



### 28.12.2020
--------------

Fuck yes, got the first images streaming back from the p1 server. The fish eye
lens is the coolest fucking thing I've ever seen. I cannot wait to make it wiggle.

Took a couple of snaps now that I have one of the lenses focused. 
![](WiggleIMG/6Focus.jpg)
![](WiggleIMG/7.jpg)


### 31.12.2020
--------------

Made a bash script to auto isntall and setup on the remaining servers. cba
typing all that out each time. 

(also it's been snowing and I made a 7ft snowman yas)

### 02.01.2021
--------------

Happy new year you filthy animal. 

I've binned the auto installing bash script and have started
using ansible instead. Ansible rips.


### 21.02.2021
--------------

I fucked off for a wee while to make a stupid mobile game and roast loads of money
off of a hedge fund. Success allround. 🚀🚀🚀

Just reaquainted myself with past-me's code. Everything was working for one camera.

I have four cameras though. so I've pinged that in the bin and started converting the
client/server to work with more than one camera.

Then will have to set up some sort of messaging system so as the main Pi can tell the 
wee pis when to take a photo/when to start previewing. 


### 21.02.2021 2
--------------

The camera is wiggling. Wiggliest camnera i've ever seen in my life. 

I accidently fed all of the cameras' data down the same network port. It's made a glitchy and
inconsistent wiggling effect. so it's an accidental bodge, but I'll take it!

I am fucking flying. 

Fish eye wiggle cams are the future of photogrophy; people will cast their wretched monoscopic
cameras into the sea once they have a look at this beauty!


### 21.02.2021 3
--------------

Wiggle preview is now implemented properly. now on to taking photos.


### 01.03.2021 
--------------

spent the last few days ripping all the threading bits apart and reorganising them. Have things 
organised a bit more than they were. still no wiggling photos to show.


### 14.09.2021 
--------------

Oh dear. I shelved this for a week and it turned into a few months and ended up being half a year. oops. 

I came back to it and binned all of the SSH code that starts the scripts running on the servers/pi minis.
The smashing thing about python is that there's always a really sick library that will do everything
you've been stressing over in three lines of code. So i've replaced it all with one of them: Paramiko. EZ.


### 14.09.2021 2
--------------

Just got the server and client to speak to each other after a day of thrashing around like a buffoon. As ever it
was really easy in the end. 
