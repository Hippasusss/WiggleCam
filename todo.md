
# IMAGE WRITING
- [x] wirte images as png to home/photos
  - [x] with the date on them
  - [x] create a folder with date to store each batch of photos
- [x] opencv create video/gif file:
  - [x] Save images
    - [x] FIX: opencv libpng IHDR error
  - [x] Save video 
    - [x] FIX: saves file but no data.
    - [x] FIX: no h.264 codec
- [x] Install opencv way to fucking hard fuck you pip
  - [x] FIX: speed up writing image to disk(?)
  - [x] only about 30mb * 4 needs to be written. Thread it. 
- [ ] Allow writing while previewing

# COMMUNICATION 
- [ ] Sending data to servers to change parameters of cameras 
  - [ ] might need confirmation to be sent back
- [ ] enusre timings between camera captures is sub 5ms ish
- [ ] make the preview more efficient 
  - [x] get rid of pygame and use opencv
  - [ ] only stream the data from the currently previewing camera 

# HARDWARE
- [ ] Design camera array holder
- [ ] Design camera array housing
- [ ] Design controller housing
  - [ ] Design/specify all the controls
- [ ] Find multipin cable to connect the two modules

# SQUISH
- [ ] client doesn't exit out of inital request
- [ ] can't send multiple requests to servers with out crash 
  - should block unitl finished? or thread it all to hell?

# LATER
- [ ] launch all python scripts at boot
- [ ] speed up boot times
- [ ] minimise cpu/battery use
  - [ ] disable bluetooth
  - [ ] disable wifi

