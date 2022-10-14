# mediapipe-bin
MediaPipe Python Wheel installer for RaspberryPi OS aarch64, Ubuntu aarch64 Debian aarch64, L4T/Jetson Nano aarch64.

## 0. Binary type
|Device|OS|Distribution|Architecture|Python ver|Numpy ver|Note|
|:--|:--|:--|:--|:--|:--|:--|
|RaspberryPi3/4|RaspberryPiOS/Debian|Buster|aarch64 / armv8|3.7.3|1.19/1.20|64bit, glibc2.28|
|RaspberryPi3/4|Ubuntu 18.04|Bionic|aarch64 / armv8|3.6.9|1.19|64bit, glibc2.27|
|RaspberryPi3/4|Ubuntu 20.04|Focal|aarch64 / armv8|3.8.2|1.19/1.20|64bit, glibc2.31|
|(Experimental/WIP) Jetson Nano|L4T (Ubuntu 18.04)|32.5.1|aarch64 / armv8|3.6.9|(mandatory) 1.19.4|64bit, glibc2.27, Pose/Holistic/Selfie Segmentation/Multi Hand Tracking/FaceDetection/FaceMesh only,OpenGL ES3.2|
|(Experimental) RaspberryPi3/4|Debian|Bullseye|aarch64 / armv8|3.9.2|1.20|64bit, glibc2.31, gcc-8.5|
|RaspberryPi3/4|Ubuntu 21.04|Hirsute|aarch64 / armv8|3.9.5|1.20|64bit, glibc2.33, gcc-7.5|

## 1. Wheels Memory swap size.
Building the full TensorFlow 2.8 package requires more than 6 Gbytes of RAM. If you have a Raspberry Pi 4 with 8 Gbyte RAM, you are in the clear. Otherwise, make sure to increase the swap size to meet this demand. With 4 Gbyte RAM onboard, zram can deliver the extra 2 Gbyte. With 2 Gbyte of RAM, you can no longer rely on zram to compress above a factor of 2. In this case, they have to reinstall dphys-swapfile to get the extra space from your SD card. Please follow the next commands if you have to install dphys-swapfile. It takes quite a while to complete the reboot when setting up swap space on a Bullseye OS.
```bash
# install dphys-swapfile
$ sudo apt-get install dphys-swapfile
# give the required memory size
$ sudo nano /etc/dphys-swapfile
# reboot afterwards
$ sudo reboot
```
<a href="https://imgur.com/UNGkGo1"><img src="https://i.imgur.com/UNGkGo1.png" title="source: imgur.com" /></a>
<a href="https://imgur.com/LMLRrap"><img src="https://i.imgur.com/LMLRrap.png" title="source: imgur.com" /></a>
<a href="https://imgur.com/5zWC1Ky"><img src="https://i.imgur.com/5zWC1Ky.png" title="source: imgur.com" /></a>
For the record, the figure shown is total amount of swap space allocated by dphys-swapfile and zram. Please, don't forget to remove dphys-swapfile when your done.

Note: if you reboot the Raspberry Pi with both zram and dphys-swapfile enabled, zram will disable dphys-swapfile during boot. You must manually reactivate this service.
```bash
# reactivate dphys-swapfile after a reboot
# (when zram and dphys-swapfile are both enabled)
$ sudo /etc/init.d/dphys-swapfile stop
$ sudo /etc/init.d/dphys-swapfile start
```
## 1. Wheels Install Opencv 4.5.5
```bash
# check your memory first
$ free -m
# you need at least a total of 6.5 GB!
# if not, enlarge your swap space as explained in the guide
$ wget https://github.com/Qengineering/Install-OpenCV-Raspberry-Pi-64-bits/raw/main/OpenCV-4-5-5.sh
$ sudo chmod 755 ./OpenCV-4-5-5.sh
$ ./OpenCV-4-5-5.sh
```
## 2. Wheels Install Tensorflow Lite
```bash
# the tools needed
$ sudo apt-get install cmake curl
# download the latest TensorFlow version (2.6.0)
$ wget -O tensorflow.zip https://github.com/tensorflow/tensorflow/archive/v2.6.0.zip
# unpack and give the folder a convenient name
$ unzip tensorflow.zip
$ mv tensorflow-2.6.0 tensorflow
$ cd tensorflow
# get the dependencies
$ ./tensorflow/lite/tools/make/download_dependencies.sh
# run the C++ installation (± 25 min)
$ ./tensorflow/lite/tools/make/build_aarch64_lib.sh
```
## 3. Bazel
### 3-1. Step1
```bash
# get a fresh start
$ sudo apt-get update
$ sudo apt-get upgrade
# install pip and pip3
$ sudo apt-get install python3-pip
# install some tools
$ sudo apt-get install zip unzip curl
# install Java
$ sudo apt-get install openjdk-11-jdk
```
### 3-1. Step2
```bash
$ wget https://github.com/bazelbuild/bazel/releases/download/4.2.1/bazel-4.2.1-dist.zip
$ unzip -d bazel bazel-4.2.1-dist.zip
$ cd bazel
```
### 3-1. Step3
During installation, Bazel uses a predefined ratio of the available working memory. This ratio is too small due to the limited size of the RAM of the Raspberry Pi. To prevent crashes, we must define the size of this memory to a maximum of 40% of the RAM onboard. For instance, 800 Mbyte for 2 GByte RAM Raspberry Pi. It is done by adding some extra information to the script file compile.sh. You can add the text ( -J-Xmx800M ) to the line that begins with run..(around line 144). See the screen below. Use the well-known <Ctrl + X>, <Y>, <Enter> to save the change (see the slide show above).
  
  <a href="https://imgur.com/3OEfJ0o"><img src="https://i.imgur.com/3OEfJ0o.png" title="source: imgur.com" /></a>

```bash
  $ nano scripts/bootstrap/compile.sh -c
``` 
```bash
-J-Xmx800M
```
### 3-1. Step3
Once the Java environment for Bazel has been maximized, you can start building the Bazel software with the next commands. When finished, copy the binary file to the /usr/local/bin location so that bash can find the executable anywhere. The final action is to delete the zip file. The total build takes about 33 minutes.
```bash
 # start the build
$ env EXTRA_BAZEL_ARGS="--host_javabase=@local_jdk//:jdk" bash ./compile.sh
# copy the binary
$ sudo cp output/bazel /usr/local/bin/bazel
# clean up
$ cd ~
$ rm bazel-4.2.1-dist.zip
# if you have a copied bazel to /usr/local/bin you may also
# delete the whole bazel directory, freeing another 500 MByte
$ sudo rm -rf bazel
``` 
<a href="https://imgur.com/6nKFSqf"><img src="https://i.imgur.com/6nKFSqf.png" title="source: imgur.com" /></a>
### MediaPipe Python Package (Unofficial) for RaspberryPi4 OS
  
 ```bash
  sudo apt install ffmpeg python3-opencv python3-pip
  ```
  ###For Raspberry Pi 4
  ###Install package
  ```bash
  sudo pip3 install mediapipe-rpi4
  ```
  To Uninstall package
  ```bash
  sudo pip3 uninstall mediapipe-rpi4
  ```
  Sometimes the protobuf package might be installed without your involvement. For this, you have two solutions to apply. Try one of the below solutions and it should work. like the Pictur
  <a href="https://imgur.com/eHW2mT0"><img src="https://i.imgur.com/eHW2mT0.png" title="source: imgur.com" /></a>
 # Solution :
You can downgrade the protobuf plugin,
  ```bash
  pip install protobuf==3.20.*
  ```
  <a href="https://imgur.com/Fszx01g"><img src="https://i.imgur.com/Fszx01g.png" title="source: imgur.com" /></a>
    ```bash
  
  ```
    ```bash
  
  ```
    ```bash
  
  ```
    ```bash
  
  ```

