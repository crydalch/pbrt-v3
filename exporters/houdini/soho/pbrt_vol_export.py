# Very rough volume exporter for pbrt v3; only exports first volume named 'density' for each object to be renderered

thisRop     = hou.pwd()
scene_file  = thisRop.parm("pbrt_diskfile").eval()
pic_file    = thisRop.parm("pbrt_picture").eval()
camera      = hou.node(thisRop.parm("camera").eval())
lights      = hou.node("/").recursiveGlob(thisRop.parm("lights").eval(), hou.nodeTypeFilter.ObjLight)
objects     = hou.node("/").recursiveGlob(thisRop.parm("objects").eval(), hou.nodeTypeFilter.ObjGeometry)

if not camera:
    raise hou.Error("A camera is required!")

pbrtfile    = open(scene_file, 'w+')
res         = camera.parmTuple("res").eval()
cam_xform   =  ' '.join(str(x) for x in camera.worldTransform().asTuple())
fov         = camera.parm("aperture").eval() # Not correct, but for now...
integrator  = thisRop.parm("pbrt_integrator").eval()
maxdepth    = thisRop.parm("pbrt_maxdepth").eval()
sampler     = thisRop.parm("pbrt_sampler").eval()
pxsamples   = thisRop.parm("pbrt_pixelsamples").eval()

# Write commented header info
pbrtfile.write('# Generated for pbrt v3 from Houdini {0}\n\n'.format(hou.applicationVersionString()))   

# Camera and render info
pbrtfile.write('Film "image" "integer xresolution" [{0}] "integer yresolution" [{1}] "string filename" "{2}"\n\n'.format(res[0],res[1],pic_file))
pbrtfile.write('Transform {0}\n'.format(cam_xform))
pbrtfile.write('Camera "perspective" "float fov" [{0}]\n'.format(fov))
pbrtfile.write('Integrator "{0}" "integer maxdepth" [{1}]\n'.format(integrator, maxdepth))
pbrtfile.write('Sampler "{0}" "integer pixelsamples" [{1}]\n\n'.format(sampler, pxsamples))

# Begin the world
pbrtfile.write('WorldBegin\n\n')

# Add lights to the scene
for lgt in lights:

    lgt_xform   = ' '.join(str(x) for x in lgt.worldTransform().asTuple())
    lgt_shape   = # Support disk and sphere for now
    lgt_L       = # The light's color * light intensity

    pbrtfile.write('AttributeBegin\n')
    pbrtfile.write('\tAreaLightSource "diffuse" "rgb L" [ {0} ]\n'.format())
    pbrtfile.write('\tTransform {0}\n'.format())
    pbrtfile.write('\Shape "{0}" "float radius" [{1}]\n'.format())
    pbrtfile.write('AttributeEnd\n')

# Add the objects to the scene
for obj in objects:
    pbrtfile.write(''.format())

# Close the world and the file
pbrtfile.write('WorldEnd\n')
pbrtfile.close()

# if '.ply' not in shapeOutputPath:
#     raise hou.Error("Must output shape to .ply file.")

# if '.pbrt' not in volOutputPath:
#     raise hou.Error("Must output volume to .pbrt file.")

# volnode     = hou.node(volpath)
# shapenode   = hou.node(shapepath)

# volgeo      = volnode.geometry()
# shapegeo    = shapenode.geometry()

# b = (shapegeo.boundingBox().minvec(), shapegeo.boundingBox().maxvec())

# # Save the volume shape to a .ply file
# shapegeo.saveToFile(shapeOutputPath)

# # Save the volume data to pbrt file
# for p in volgeo.prims():
#     if isinstance(p, hou.Volume) and p.attribValue('name') == 'density':
#         vf = open(volOutputPath, 'w+')
#         res = p.resolution()
#         nx = res[0]
#         ny = res[1]
#         nz = res[2]
#         vf.write('MakeNamedMedium "{0}" "string type" "heterogeneous" "integer nx" {1} "integer ny" {2} "integer nz" {3}\n'.format(mediumName, nx, ny, nz) )
#         vf.write('    "point p0" [ {0} {1} {2} ] "point p1" [ {3} {4} {5} ]\n'.format(b[0][0], b[0][1], b[0][2], b[1][0], b[1][1], b[1][2]))
#         vf.write('    "float density" [\n')
#         for rz in range(nz):
#             for ry in range(ny):
#                 for rx in range(nx):
#                     vf.write('{0} '.format(p.voxel((rx,ry,rz))))
#                 vf.write('\n')
#         vf.write(']')
#         vf.close()
#         break