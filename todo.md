
# IMAGE WRITING
- [x] wirte images as png to home/photos
  - [x] with the date on them
  - [x] create a folder with date to store each batch of photos
- [ ] opencv create video/gif file:
  - [ ] FIX: video saving as black 
  - [ ] FIX: opencv libpng IHDR error
  - [ ] make changing framerate etc easy
- [x] Install opencv way to fucking hard fuck you pip
  - [ ] FIX: speed up writing image to disk(?)
  - [ ] only about 30mb * 4 needs to be written. Thread it. 

# COMMUNICATION 
    - [ ] Sending data to servers to change parameters of cameras 
        - [ ] might need confirmation to be sent back

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

