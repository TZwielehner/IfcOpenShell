cobie_type_classes = [
    "IfcDoorStyle",
    "IfcBuildingElementProxyType",
    "IfcChimneyType",
    "IfcCoveringType",
    "IfcDoorType",
    "IfcFootingType",
    "IfcPileType",
    "IfcRoofType",
    "IfcShadingDeviceType",
    "IfcWindowType",
    "IfcDistributionControlElementType",
    "IfcDistributionChamberElementType",
    "IfcEnergyConversionDeviceType",
    "IfcFlowControllerType",
    "IfcFlowMovingDeviceType",
    "IfcFlowStorageDeviceType",
    "IfcFlowTerminalType",
    "IfcFlowTreatmentDeviceType",
    "IfcElementAssemblyType",
    "IfcBuildingElementPartType",
    "IfcDiscreteAccessoryType",
    "IfcMechanicalFastenerType",
    "IfcReinforcingElementType",
    "IfcVibrationIsolatorType",
    "IfcFurnishingElementType",
    "IfcGeographicElementType",
    "IfcTransportElementType",
    "IfcSpatialZoneType",
    "IfcWindowStyle",
]

cobie_component_classes = [
    "IfcBuildingElementProxy",
    "IfcChimney",
    "IfcCovering",
    "IfcDoor",
    "IfcShadingDevice",
    "IfcWindow",
    "IfcDistributionControlElement",
    "IfcDistributionChamberElement",
    "IfcEnergyConversionDevice",
    "IfcFlowController",
    "IfcFlowMovingDevice",
    "IfcFlowStorageDevice",
    "IfcFlowTerminal",
    "IfcFlowTreatmentDevice",
    "IfcDiscreteAccessory",
    "IfcTendon",
    "IfcTendonAnchor",
    "IfcVibrationIsolator",
    "IfcFurnishingElement",
    "IfcGeographicElement",
    "IfcTransportElement",
]

fmhem_classes = [
    "IfcDoorStyle",
    "IfcWindowStyle",
    "IfcDoorType",
    "IfcWindowType",
    "IfcRoofType",
    "IfcShadingDeviceType",
    "IfcDistributionControlElementType",
    "IfcEnergyConversionDeviceType",
    "IfcFlowControllerType",
    "IfcJunctionBoxType",
    "IfcFlowMovingDeviceType",
    "IfcFlowStorageDeviceType",
    "IfcFlowTerminalType",
    "IfcFlowTreatmentDeviceType",
    "IfcFurnishingElementType",
    "IfcTransportElementType",
]


def get_cobie_types(ifc_file):
    elements = []
    for ifc_class in cobie_type_classes:
        try:
            elements += self.file.by_type(ifc_class)
        except:
            pass
    return elements


def get_cobie_components(ifc_file):
    elements = []
    for ifc_class in cobie_component_classes:
        try:
            elements += self.file.by_type(ifc_class)
        except:
            pass
    return elements


def get_fmhem_types(ifc_file):
    elements = []
    for ifc_class in fmhem_classes:
        try:
            if ifc_class == "IfcEnergyConversionDeviceType":
                elements += [e for e in ifc_file.by_type(ifc_class) if not e.is_a("IfcCooledBeamType")]
            else:
                elements += ifc_file.by_type(ifc_class)
        except:
            pass
    return elements
