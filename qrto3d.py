import bpy

# ADD-ON UI
class QRto3DSettings(bpy.types.PropertyGroup):
    filepath: bpy.props.StringProperty(
                name='',
                description='Path to QR file',
                default='',
                maxlen=1024,
                subtype='FILE_PATH')
    cubesize: bpy.props.IntProperty(
                name='',
                description='Cube Size used during QR generation',
                default=1,
                max=4,
                min=1)
    border: bpy.props.BoolProperty(
                name='',
                description='Generate QR with raised border',
                default=False)

class SCENE_PT_QRto3D(bpy.types.Panel):
    bl_label = 'QR to 3D'
    bl_idname= 'SCENE_PT_QRto3D'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'scene'
    
    def draw(self, context):
        scene = context.scene
        layout = self.layout
        
        qrFileName = layout.row()
        qrFileName.prop(scene.filepath, 'filepath', text='File Path')
        
        qrProps = layout.row()
        qrProps.prop(scene.cubesize, 'cubesize', text='Cube Size')
        qrProps.prop(scene.border, 'border', text='Border')
        
        qrGenerate = layout.row()
        qrGenerate.operator('mesh.qrto3d')
        
# QR GENERATION OPERATOR
class GenerateQRFromFile(bpy.types.Operator):
    bl_label = 'Generate QR'
    bl_idname = 'mesh.qrto3d'   

    def cleanRows(self, qrRows):
        qrRows.pop()
        for row in enumerate(qrRows):
            qrRows[row[0]] = row[1][2:len(row[1])-1]
        return qrRows

    def isPartOfBorder(self, borderEnabled, row, cube, rowMax, cubeMax):
        if borderEnabled:
            if row[0] == 0 or row[0] == rowMax or cube[0] == 0 or cube[0] == cubeMax:
                return True
        return False

    def execute(self, context):
        scene = context.scene 
        cube_size = scene.cubesize.cubesize
        borderEnabled = scene.border.border  
        
        filepath = str(scene.filepath.filepath)
        if filepath:
                if filepath.endswith('.array'):
                    # create parent QR object
                    qrObject = bpy.data.objects.new('QRObject', None)
                    bpy.context.collection.objects.link(qrObject)
                    
                    # read .array file
                    qrArrayFile = open(filepath, 'r')
                    qrArrayFile.seek(0)
                    qrArrayAsStr = qrArrayFile.readlines()[0]
                    qrArrayFile.close()

                    # format array of QR rows
                    qrRows = qrArrayAsStr.split(']')
                    qrRows = self.cleanRows(qrRows)
                    
                    # create base plane
                    qrWidthInCubes = len(qrRows[0]) * cube_size
                    bpy.ops.mesh.primitive_plane_add(location=(qrWidthInCubes/2,qrWidthInCubes/2,0), size=qrWidthInCubes)
                    bpy.ops.object.modifier_add(type='SOLIDIFY')
                    
                    base_plane = bpy.context.active_object
                    base_plane.modifiers['Solidify'].thickness = 1
                    base_plane.parent = qrObject                

                    # create QR model
                    for row in enumerate(reversed(qrRows)):
                        tempRow = [cube for cube in row[1]]
                        for cube in enumerate(tempRow):
                            if cube[1] != '0' or self.isPartOfBorder(borderEnabled, row, cube, len(qrRows)-1, len(tempRow)-1):
                                bpy.ops.mesh.primitive_cube_add(location=((cube[0]*cube_size)+cube_size/2, (row[0]*cube_size)+cube_size/2, cube_size/2), size=cube_size)
                                bpy.context.active_object.parent = qrObject   
                else:
                    print('invalid file type')                                             
        else:
            print('invalid filepath')
            
        return {'FINISHED'}
        
# REGISTER CLASSES
classes = (
    QRto3DSettings,
    SCENE_PT_QRto3D,
    GenerateQRFromFile
)
        
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.filepath = bpy.props.PointerProperty(type=QRto3DSettings)
    bpy.types.Scene.cubesize = bpy.props.PointerProperty(type=QRto3DSettings)
    bpy.types.Scene.border = bpy.props.PointerProperty(type=QRto3DSettings)
    
def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
        
    del bpy.types.Scene.filepath
    del bpy.types.Scene.cubesize
    del bpy.types.Scene.border
    
if __name__ == "__main__":
    register()