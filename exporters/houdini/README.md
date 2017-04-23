# Houdini PBRT Export

Plugins and HDAs for rendering data from Houdini using pbrt.

# Requirements

Currently, because the HDA is a non-commerical asset, and third-party rendering requires a full commercial license or an education license, you can only render with an Education license. 

If your school/institution does not have one, contact SideFX (education@sidefx.com).

# Installation

Either add  `exporter/houdini` path to `$HOUDINI_PATH`, or copy the folders and contents of the __config__, __soho__, and __otls__ directories to your *$HOME/houdiniXX.YY* folder.

If those directories don't exist, create them.

# Usage

Simply point to the volume geometry you want to export, and choose where to save your .pbrt file. It currently is intended to add volumes to a scene by including the generated pbrt file into your scene with a text editor.

It will include the translation/rotation of the geometry's object container, so make sure that's where you camera would be.

When you click _Save to Disk_, it will generate a file which appears something like this:

```
#
# Generated for pbrt v3 from Houdini 16.0.557
# Add this volume to a pbrt scene manually, using a relative or absolute path:
#
#    Include "mytestb.pbrt"
#    Include "/tmp/mytestb.pbrt"
#

AttributeBegin
    Translate 0.0 0.0 0.0
    Rotate 45.0 0.0 1.0 0.0
    MakeNamedMedium "mysmoke" "string type" "heterogeneous" "integer nx" 9 "integer ny" 10 "integer nz" 8
        "point p0" [ -0.457499951124 -0.502499997616 -0.412499964237 ] "point p1" [ 0.412500053644 0.482500016689 0.412500023842 ]
        "float density" [
            0.0 0.0 0.0 0.0 0.000256679253653 0.0 0.00966993812472 0.00130098487716 0.0 
            0.0 0.0 0.0 0.0197598207742 0.15717124939 0.0705833807588 0.00709029799327 0.0 0.0 
            ...
            0.0 0.0 0.0 0.000708940555342 0.0751384869218 0.0470002889633 0.0 0.0 0.0 
            0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 
            0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 
            ]
        "rgb sigma_a" [10.0 10.0 10.0] "rgb sigma_s" [190.0 190.0 190.0]
    Material ""
    MediumInterface "mysmoke" ""
    Shape "trianglemesh"
        "point P" [
          0.412500053644 -0.502499997616 0.412500023842
          -0.457499951124 -0.502499997616 0.412500023842
          -0.457499951124 0.482500016689 0.412500023842
          0.412500053644 0.482500016689 0.412500023842
          -0.457499951124 -0.502499997616 -0.412499964237
          0.412500053644 -0.502499997616 -0.412499964237
          0.412500053644 0.482500016689 -0.412499964237
          -0.457499951124 0.482500016689 -0.412499964237
        ]
        "integer indices" [
          0 1 2
          0 3 1
          4 5 6
          4 7 5
          7 3 5
          7 1 3
          6 2 4
          6 0 2
          6 3 0
          6 5 3
          2 7 4
          2 1 7
        ]
AttributeEnd
```