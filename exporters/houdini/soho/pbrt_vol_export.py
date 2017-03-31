# Very rough volume exporter for pbrt v3; only exports first volume named 'density'
from sohog import SohoGeometry

volpath     = hou.pwd().parm("volpath").eval()
shapepath   = hou.pwd().parm("shapepath").eval()
shapeOutputPath = hou.pwd().parm("shapeoutput").eval()
volOutputPath = hou.pwd().parm("voloutput").eval()
shapeOutputFileName = shapeOutputPath.split("/")[-1]
mediumName = hou.pwd().parm("mediumName").eval()

if '.ply' not in shapeOutputPath:
    raise hou.Error("Must output shape to .ply file.")

if '.pbrt' not in volOutputPath:
    raise hou.Error("Must output volume to .pbrt file.")

volnode     = hou.node(volpath)
shapenode   = hou.node(shapepath)

volgeo      = volnode.geometry()
shapegeo    = shapenode.geometry()

b = (shapegeo.boundingBox().minvec(), shapegeo.boundingBox().maxvec())

# Save the volume shape to a .ply file
shapegeo.saveToFile(shapeOutputPath)

# Save the volume data to pbrt file
for p in volgeo.prims():
    if isinstance(p, hou.Volume) and p.attribValue('name') == 'density':
        vf = open(volOutputPath, 'w+')
        res = p.resolution()
        nx = res[0]
        ny = res[1]
        nz = res[2]
        vf.write('MakeNamedMedium "{0}" "string type" "heterogeneous" "integer nx" {1} "integer ny" {2} "integer nz" {3}\n'.format(mediumName, nx, ny, nz) )
        vf.write('    "point p0" [ {0} {1} {2} ] "point p1" [ {3} {4} {5} ]\n'.format(b[0][0], b[0][1], b[0][2], b[1][0], b[1][1], b[1][2]))
        vf.write('    "float density" [\n')
        for rz in range(nz):
            for ry in range(ny):
                for rx in range(nx):
                    vf.write('{0} '.format(p.voxel((rx,ry,rz))))
                vf.write('\n')
        vf.write(']')
        vf.close()