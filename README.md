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
### 3-1. Step4
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

### 3-2. Jetson Nano + L4T 32.5.1 64bit (aarch64) + Python3.6 + GPU (22.0FPS)
```bash
$ cd ~
$ git clone https://github.com/Kazuhito00/mediapipe-python-sample && cd mediapipe-python-sample
$ python3 sample_hand.py
```


## 4. Build
### 4-1. Other than Jetson Nano
```bash
$ sudo apt update && \
  sudo apt install -y \
  python3-dev cmake protobuf-compiler \
  python3-pip git make openjdk-11-jdk-headless

$ sudo pip3 install pip setuptools --upgrade

$ git clone -b v0.8.4 https://github.com/google/mediapipe && cd mediapipe

$ sed -i -e "/\"imgcodecs\"/d;/\"calib3d\"/d;/\"features2d\"/d;/\"highgui\"/d;/\"video\"/d;/\"videoio\"/d" third_party/BUILD
$ sed -i -e "/-ljpeg/d;/-lpng/d;/-ltiff/d;/-lImath/d;/-lIlmImf/d;/-lHalf/d;/-lIex/d;/-lIlmThread/d;/-lrt/d;/-ldc1394/d;/-lavcodec/d;/-lavformat/d;/-lavutil/d;/-lswscale/d;/-lavresample/d" third_party/BUILD

$ sed -i -e "/^        # Optimization flags/i \        \"ENABLE_NEON\": \"OFF\"," third_party/BUILD
$ sed -i -e "/^        # Optimization flags/i \        \"WITH_TENGINE\": \"OFF\"," third_party/BUILD

$ wget https://github.com/PINTO0309/Bazel_bin/raw/main/3.7.2/aarch64/install.sh
$ sudo chmod +x install.sh
$ ./install.sh

$ sudo python3 setup.py gen_protos
$ sudo bazel clean --expunge
$ sudo python3 setup.py bdist_wheel
```
### 4-2. (Experimental / WIP) Jetson Nano
- **[Verification of mediapipe's GPU-enabled .pbtxt processing method](https://zenn.dev/pinto0309/scraps/71368ef3d74438)**

### 4-3. opencv_contrib_python-4.5.* 
- **[Build the Wheel installer for opencv-contrib-python](https://qengineering.eu/install-opencv-4.5-on-jetson-nano.html)**
- **[Build the Wheel installer for opencv-contrib-python](https://zenn.dev/pinto0309/scraps/e10bc3a8be82f1)**


## 5. Reference
1. I was inspired by **[jiuqiant's](https://github.com/jiuqiant/mediapipe_python_aarch64)** **[mediapipe_python_aarch64](https://github.com/jiuqiant/mediapipe_python_aarch64)** to create this repository. Thank you so much! 🌠
2. Article: **[How to enjoy MediaPipe easily with Raspberry Pi - karaage0703 - Zenn](https://zenn.dev/karaage0703/articles/63fed2a261096d)** 🌟
3. Sample: **[mediapipe-python-sample - Kazuhito00 - GitHub](https://github.com/Kazuhito00/mediapipe-python-sample)** 🌟
4. OS Image: **https://downloads.raspberrypi.org/raspios_arm64/images/raspios_arm64-2021-05-28/**
