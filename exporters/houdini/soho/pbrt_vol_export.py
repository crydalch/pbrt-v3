# Very rough volume exporter for pbrt v3
#
#   Save volume(s) to pbrt file on-disk, optionally with the Obj-level transform applied
#   Only exports volumes named 'density' for now
#
#

# Thanks graham
def findParentObject(node):
    """ Find the first parent node that is an object node. """
    # The node is an object node so return it.
    if isinstance(node, hou.ObjNode):
        return node
    # Get the parent of the node.
    parent = node.parent()
    # If there is no parent then we have failed, so return None.
    if not parent:
        return None
    # Check the parent node.
    return findParentObject(parent)

thisRop         = hou.pwd()
volOutputPath   = thisRop.parm("pbrt_vol_diskfile").eval()
sopPath         = thisRop.parm("soppath").eval()

sigma_a         = " ".join([str(x) for x in thisRop.parmTuple("pbrt_sigma_a").eval()])
sigma_s         = " ".join([str(x) for x in thisRop.parmTuple("pbrt_sigma_s").eval()])
phase_g         = thisRop.parm("pbrt_g").eval()
mediumName      = thisRop.parm("pbrt_mediumName").eval()

vf = open(volOutputPath, 'w+')

q           = hou.Quaternion()
volnode     = hou.node(sopPath)
volgeo      = volnode.geometry()
volobj      = findParentObject(volnode)
volobjxform = volobj.worldTransform().explode()
q.setToRotationMatrix(volobj.worldTransform())
volt        = volobjxform['translate']
volr        = q.extractAngleAxis()

if not volgeo.containsPrimType("Volume"):
    raise hou.Error('No volumes detected on the input SOP.')

b = (volgeo.boundingBox().minvec(), volgeo.boundingBox().maxvec())

# Just for organization
_min = b[0]
_max = b[1]

# # Save the volume shape to a .ply file
# shapegeo.saveToFile(shapeOutputPath)

vf.write('#\n# Generated for pbrt v3 from Houdini {0}\n'.format(hou.applicationVersionString()))
vf.write('# Add this volume to a pbrt scene manually, using a relative or absolute path:\n#\n')
vf.write('#    Include "{0}"\n'.format(volOutputPath.split('/')[-1]))   
vf.write('#    Include "{0}"\n#\n\n'.format(volOutputPath))

# Save the volume data to pbrt file
for p in volgeo.prims():
    if isinstance(p, hou.Volume) and p.attribValue('name') == 'density':
        vf.write('AttributeBegin\n')
        # Probably want to just stuff the transform here, instead of breaking it apart
        vf.write('    Translate {0} {1} {2}\n'.format(volt[0], volt[1], volt[2]))
        vf.write('    Rotate {0} {1} {2} {3}\n'.format(volr[0], volr[1][0], volr[1][1], volr[1][2]))
        res = p.resolution()
        nx = res[0]
        ny = res[1]
        nz = res[2]
        vf.write('    MakeNamedMedium "{0}" "string type" "heterogeneous" "integer nx" {1} "integer ny" {2} "integer nz" {3}\n'.format(mediumName, nx, ny, nz) )
        vf.write('        "point p0" [ {0} {1} {2} ] "point p1" [ {3} {4} {5} ]\n'.format(b[0][0], b[0][1], b[0][2], b[1][0], b[1][1], b[1][2]))
        vf.write('        "float density" [\n            ')
        for rz in range(nz):
            for ry in range(ny):
                for rx in range(nx):
                    vf.write('{0} '.format(p.voxel((rx,ry,rz))))
                vf.write('\n            ')
        vf.write(']\n')
        vf.write('        "rgb sigma_a" [{0}] "rgb sigma_s" [{1}]\n'.format(sigma_a, sigma_s))
        vf.write('    Material ""\n')
        vf.write('    MediumInterface "{0}" ""\n'.format(mediumName))
        vf.write('    Shape "trianglemesh"\n')
        vf.write('        "point P" [\n')
        vf.write('          {0} {1} {2}\n'.format(_max[0], _min[1], _max[2]))
        vf.write('          {0} {1} {2}\n'.format(_min[0], _min[1], _max[2]))
        vf.write('          {0} {1} {2}\n'.format(_min[0], _max[1], _max[2]))
        vf.write('          {0} {1} {2}\n'.format(_max[0], _max[1], _max[2]))
        vf.write('          {0} {1} {2}\n'.format(_min[0], _min[1], _min[2]))
        vf.write('          {0} {1} {2}\n'.format(_max[0], _min[1], _min[2]))
        vf.write('          {0} {1} {2}\n'.format(_max[0], _max[1], _min[2]))
        vf.write('          {0} {1} {2}\n'.format(_min[0], _max[1], _min[2]))
        vf.write('        ]\n')
        vf.write('        "integer indices" [\n')
        vf.write('          0 1 2\n')
        vf.write('          0 3 1\n')
        vf.write('          4 5 6\n')
        vf.write('          4 7 5\n')
        vf.write('          7 3 5\n')
        vf.write('          7 1 3\n')
        vf.write('          6 2 4\n')
        vf.write('          6 0 2\n')
        vf.write('          6 3 0\n')
        vf.write('          6 5 3\n')
        vf.write('          2 7 4\n')
        vf.write('          2 1 7\n')
        vf.write('        ]\n')
        break
vf.write('AttributeEnd\n')
vf.close()      
