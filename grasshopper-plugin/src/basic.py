#!/usr/bin/env ipy
# -*- coding: utf-8 -*-

__all__ = ['Handshake_Component']

# - - - - - - - - BUILT-IN IMPORTS
import System
import traceback

# - - - - - - - - LOCAL IMPORTS
import tapir
from tapir_py import core

# - - - - - - - - RH/GH IMPORTS
from ghpythonlib.componentbase import dotnetcompiledcomponent as component
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML
import Rhino, Grasshopper, GhPython

# - - - - - - - - COMPONENT
class Handshake_Component(component):

    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Handshake", "Handshake", """Establishes connection between current Grasshopper document, and any open ArchiCAD project.""", "tAPIr", "01 Connect")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("bb340f32-83f5-4140-9956-960003773db4")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "Refresh", "R", "Refreshes the link to the ArchiCAD project.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "Link", "A", "ArchiCAD Command Object, that can execute commands.")
        self.Params.Output.Add(p)
        
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        result = self.RunScript(p0)

        if result is not None:
            self.marshal.SetOutput(result, DA, 0, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAFiUAABYlAUlSJPAAAADJSURBVEhL7ZNbDsQgCEV1/4vu8PYCpm0yyfyMJzFeEARMOw7/whyXKWOifU1avKtJSDzGhJY4i08UR0oAzN8KRNzylaaTkS9KuP20M6jZkEttpQl0ZC2mfiu8niLFK6m51um7CeCtd/GgXxfY+klvJrgvEPazX3PBL8XW+W+QLiZ+v9hB1WGX7911/2+IZNiYjmp8xqXrTqTcgJ0wQbwjLUvAKa0A6gXmFmBkPOw+LCBg17sJrDtSftgTcqeioSHGNe++DoevGeMDe+h/wjhtikQAAAAASUVORK5CYII="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    def __init__(self):
        self.is_valid = False
        self.archicad = None

    def RunScript(self, refresh):
        
        if refresh:
            self.archicad = core.Command.create()
            self.is_valid = self.archicad.IsAlive()
        
        tapir.Plugin.is_active = self.is_valid

        if self.is_valid:
            tapir.Plugin.Archicad = self.archicad
            self.Message = "Port: {}".format(self.archicad.link.port)
            return self.archicad
        
        else:
            tapir.Plugin.Archicad = None
            self.Message = ""
            self.AddRuntimeMessage(RML.Warning, "Connection Failed: Unable to connect to ArchiCAD.")
            return None
    
    def on_disconnect_click(self, sender, args):
        try:
            self.__init__()
            self.ExpireSolution(True)
        except Exception as ex:
            System.Windows.Forms.MessageBox.Show(traceback.format_exc(), ex)

    def AppendAdditionalMenuItems(self , items):
        component.AppendAdditionalMenuItems(self , items)
        try:
            disconnect_menu_item = items.Items.Add('Disconnect', None, self.on_disconnect_click)
        except Exception as ex:
            System.Windows.Forms.MessageBox.Show(traceback.format_exc(), ex)



# TODO: ProjectInfo / ProductInfo / 