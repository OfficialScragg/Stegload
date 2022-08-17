# Stegload

Load a text-based payload into an image for anti-virus evasion and then extract the payload for execution on the target host.

Stegload implements the most basic form of information hiding in image files.
Least significant bits in the RGB values of each pixel are toggled to represent a bit of the hidden data.
The data can then be retrieved by extracting and compiling the last bit of each R, G and B value from each pixel.
