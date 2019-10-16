import bpy
import json
import os

cwd = os.path.dirname(os.path.realpath(__file__)) + os.path.sep

class IfcSchema():
    def __init__(self):
        with open('{}ifc_elements_IFC4.json'.format(cwd + 'schema/')) as f:
            self.elements = json.load(f)

ifc_schema = IfcSchema()

class BIMProperties(bpy.types.PropertyGroup):
    def getIfcClasses(self, context):
        return [(e, e, '') for e in ifc_schema.elements]

    def getIfcPredefinedTypes(self, context):
        results = []
        for name, data in ifc_schema.elements.items():
            if name != bpy.context.scene.BIMProperties.ifc_class:
                continue
            for attribute in data['attributes']:
                if attribute['name'] != 'PredefinedType':
                    continue
                return [(e, e, '') for e in attribute['enum_values']]

    def getPsetNames(self, context):
        files = os.listdir(bpy.context.scene.BIMProperties.data_dir + 'pset/')
        return [(f, f, '') for f in files]

    def getPsetFiles(self, context):
        if not bpy.context.scene.BIMProperties.pset_name:
            return []
        files = os.listdir(bpy.context.scene.BIMProperties.data_dir + 'pset/{}/'.format(bpy.context.scene.BIMProperties.pset_name))
        return [(f.replace('.csv', ''), f.replace('.csv', ''), '') for f in files]

    schema_dir: bpy.props.StringProperty(default=cwd + 'schema/', name="Schema Directory")
    data_dir: bpy.props.StringProperty(default=cwd + 'data/', name="Data Directory")
    ifc_class: bpy.props.EnumProperty(items = getIfcClasses, name="Class")
    ifc_predefined_type: bpy.props.EnumProperty(
        items = getIfcPredefinedTypes,
        name="Predefined Type", default=None)
    ifc_userdefined_type: bpy.props.StringProperty(name="Userdefined Type")
    export_has_representations: bpy.props.BoolProperty(name="Export Representations", default=True)
    qa_reject_element_reason: bpy.props.StringProperty(name="Element Rejection Reason")
    pset_name: bpy.props.EnumProperty(items=getPsetNames, name="Pset Name")
    pset_file: bpy.props.EnumProperty(items=getPsetFiles, name="Pset File")

class Attribute(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Name")
    data_type: bpy.props.StringProperty(name="Data Type")
    string_value: bpy.props.StringProperty(name="Value")
    bool_value: bpy.props.BoolProperty(name="Value")
    int_value: bpy.props.IntProperty(name="Value")
    float_value: bpy.props.FloatProperty(name="Value")

class ObjectProperties(bpy.types.PropertyGroup):
    attributes: bpy.props.CollectionProperty(name="Attributes", type=Attribute)

class MaterialProperties(bpy.types.PropertyGroup):
    is_external: bpy.props.BoolProperty(name="Has External Definition")
    location: bpy.props.StringProperty(name="Location")
    identification: bpy.props.StringProperty(name="Identification")
    name: bpy.props.StringProperty(name="Name")

class MeshProperties(bpy.types.PropertyGroup):
    is_wireframe: bpy.props.BoolProperty(name="Is Wireframe")
    is_swept_solid: bpy.props.BoolProperty(name="Is Swept Solid")

class ObjectPanel(bpy.types.Panel):
    bl_label = 'IFC Object'
    bl_idname = 'BIM_PT_object'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'object'

    def draw(self, context):
        if not bpy.context.active_object:
            return
        layout = self.layout
        layout.label(text="Software Identity:")
        row = layout.row()
        row.operator('bim.generate_global_id')

        layout.label(text="Attributes:")
        row = layout.row()
        row.operator('bim.add_attribute')

        for index, attribute in enumerate(bpy.context.active_object.ObjectProperties.attributes):
            row = layout.row(align=True)
            row.prop(attribute, 'name', text='')
            row.prop(attribute, 'string_value', text='')
            row.operator('bim.remove_attribute', icon='CANCEL', text='').attribute_index = index

        row = layout.row()
        row.prop(bpy.context.active_object.ObjectProperties, 'attributes')

class MeshPanel(bpy.types.Panel):
    bl_label = 'IFC Representations'
    bl_idname = 'BIM_PT_mesh'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'

    def draw(self, context):
        if not bpy.context.active_object.data:
            return
        layout = self.layout
        row = layout.row()
        row.prop(bpy.context.active_object.data.MeshProperties, 'is_wireframe')
        row = layout.row()
        row.prop(bpy.context.active_object.data.MeshProperties, 'is_swept_solid')
        row = layout.row(align=True)
        row.operator('bim.assign_swept_solid_profile')
        row.operator('bim.assign_swept_solid_extrusion')

class MaterialPanel(bpy.types.Panel):
    bl_label = 'IFC Materials'
    bl_idname = 'BIM_PT_material'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'material'

    def draw(self, context):
        if not bpy.context.active_object.active_material:
            return
        layout = self.layout
        row = layout.row()
        row.prop(bpy.context.active_object.active_material.MaterialProperties, 'is_external')
        row = layout.row(align=True)
        row.prop(bpy.context.active_object.active_material.MaterialProperties, 'location')
        row.operator('bim.select_external_material_dir', icon="FILE_FOLDER", text="")
        row = layout.row()
        row.prop(bpy.context.active_object.active_material.MaterialProperties, 'identification')
        row = layout.row()
        row.prop(bpy.context.active_object.active_material.MaterialProperties, 'name')

class BIMPanel(bpy.types.Panel):
    bl_label = "Building Information Modeling"
    bl_idname = "BIM_PT_bim"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        bim_properties = bpy.context.scene.BIMProperties

        layout.label(text="System Setup:")

        col = layout.column()
        row = col.row(align=True)
        row.prop(bim_properties, "schema_dir")
        row.operator("bim.select_schema_dir", icon="FILE_FOLDER", text="")

        col = layout.column()
        row = col.row(align=True)
        row.prop(bim_properties, "data_dir")
        row.operator("bim.select_data_dir", icon="FILE_FOLDER", text="")

        layout.label(text="IFC Categorisation:")

        row = layout.row()
        row.prop(bim_properties, "ifc_class")
        row = layout.row()
        row.prop(bim_properties, "ifc_predefined_type")
        row = layout.row()
        row.prop(bim_properties, "ifc_userdefined_type")
        row = layout.row()
        row.operator("bim.assign_class")

        row = layout.row(align=True)
        row.operator("bim.select_class")
        row.operator("bim.select_type")

        layout.label(text="Property Sets:")
        row = layout.row()
        row.prop(bim_properties, "pset_name")
        row = layout.row()
        row.prop(bim_properties, "pset_file")

        row = layout.row(align=True)
        row.operator("bim.assign_pset")
        row.operator("bim.remove_pset")

        layout.label(text="Quality Auditing:")

        row = layout.row()
        row.prop(bim_properties, "qa_reject_element_reason")
        row = layout.row()
        row.operator("bim.reject_element")

        row = layout.row(align=True)
        row.operator("bim.colour_by_class")
        row.operator("bim.reset_object_colours")

        row = layout.row(align=True)
        row.operator("bim.approve_class")
        row.operator("bim.reject_class")

        row = layout.row()
        row.operator("bim.select_audited")

class MVDPanel(bpy.types.Panel):
    bl_label = "Model View Definitions"
    bl_idname = "BIM_PT_mvd"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        bim_properties = bpy.context.scene.BIMProperties

        layout.label(text="Custom MVD:")

        row = layout.row()
        row.prop(bim_properties, "export_has_representations")
