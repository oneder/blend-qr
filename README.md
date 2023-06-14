# blend-qr
Blender add-on to generate 3D QR codes

# url_gen.py
This script generates a QR code for a given URL, exporting both a \*.array file (containing QR data to be used within the Blender add-on), and a graphical representation in either PNG or SVG format. This script is intended to be run outside of Blender and can be thought of as an independent utility for generating QR codes locally, fast, in addition to generating the data files to be consumed by the Blender add-on (see below).

# qrto3d.py
This script is the code behind the Blender add-on to generate 3D QR codes. The add-on, <i>QR to 3D</i>, reads the \*.array files exported by the QR generation utility script (above) and generates a 3D represenation (with a user-defined cube size) within the the 3D Window. The add-on also supports generating the QR code with and without a border.

<b>How to Run:</b><br>
Install <a href="https://www.blender.org/" target="_blank">Blender</a>.

Follow <a href="https://blender.stackexchange.com/questions/154597/running-blender-from-the-command-line#:~:text=If%20you%20already%20know%20Blender%27s%20install%20directory%3A%201,to%20change%20the%20directory%2C%20for%20example%20cd%20K%3A%5C05_Download%5Cblender-2.80-windows64" target="_blank">these</a> steps to run Blender from terminal.

In Blender, navigate to the <i>Scripting</i> tab and open your local version of the script in the Blender code editor window.

Run it, and verify the <i>QR to 3D</i> panel has been added to the Scene Properties window.

Using the new add-on, select the \*.array file for the specific QR code you would like to model, set the cube size (default=1) and border preference, and the click <i>Generate QR</i>.
