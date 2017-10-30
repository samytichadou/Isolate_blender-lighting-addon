# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; version 3
#  of the License.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


bl_info = {  
 "name": "Isolate",  
 "author": "Samy Tichadou (tonton)",  
 "version": (0, 4),  
 "blender": (2, 7, 9),  
 "location": "3d View > Down Header",  
 "description": "Isolate Lamps",  
  "wiki_url": "https://github.com/samytichadou/Isolate_blender-lighting-addon/wiki",  
 "tracker_url": "https://github.com/samytichadou/Isolate_blender-lighting-addon/issues/new",  
 "category": "Lighting"}
 
import bpy
import blf
import bgl
from bpy_extras.view3d_utils import location_3d_to_region_2d
        
        
#######################################################################
### addon preferences ###
#######################################################################

class IsolateLightAddonPrefs(bpy.types.AddonPreferences):
    bl_idname = __name__
            
    prefs_base = bpy.props.FloatVectorProperty(name="Base Color", 
                                        subtype='COLOR', 
                                        default=[1.0, 1.0, 1.0])
                                        
    prefs_highlight = bpy.props.FloatVectorProperty(name="HighLight Color", 
                                        subtype='COLOR', 
                                        default=[1.0, 1.0, 0.0])
                                        
    prefs_lamp = bpy.props.FloatVectorProperty(name="Lamp Color", 
                                        subtype='COLOR', 
                                        default=[1.0, 0.0, 1.0])
                                        
    prefs_meshlight = bpy.props.FloatVectorProperty(name="MeshLight Color", 
                                        subtype='COLOR', 
                                        default=[0.0, 0.0, 1.0])
                                        
    prefs_border = bpy.props.FloatVectorProperty(name="MeshLight Color", 
                                        subtype='COLOR', 
                                        default=[1.0, 1.0, 1.0])
                
    def draw(self, context):
        layout = self.layout
        layout.label('Viewport Colors :', icon='COLOR')
        row=layout.row(align=True)
        row.prop(self, "prefs_base", expand=False, text='Base')
        row.prop(self, "prefs_highlight", expand=False, text='HighLight')
        row.prop(self, "prefs_border", expand=False, text='Border')
        row.prop(self, "prefs_lamp", expand=False, text='Lamp')
        row.prop(self, "prefs_meshlight", expand=False, text='MeshLight')
              
        
# get addon preferences
def get_addon_preferences():
    addon_preferences = bpy.context.user_preferences.addons[__name__].preferences
    return addon_preferences

#######################################################################
### modal operators ###
#######################################################################

def draw_callback_light(self, context):
    winman=bpy.data.window_managers['WinMan']
    addon_preferences = get_addon_preferences()
    isolated=[]
    notvisible=[]
    hidden=[]
    location=[]
    oklocation=[]
    lamps=[]
    lights=[]
    meshisolated=[]
    meshnotvisible=[]
    meshhidden=[]
    meshoklocation=[]
    mesh=[]
    slayers=[]
    size=winman.isolatelight_font_size
    space=winman.isolatelight_font_space
    layer=winman.isolatelight_layer_modal
    lampIO=winman.isolatelight_lamp_onoff_modal
    meshIO=winman.isolatelight_meshlight_onoff_modal
    mx=winman.isolatelight_mx
    my=winman.isolatelight_my
    hover=0
    surlign=(*addon_preferences.prefs_highlight, 1.0)
    wh=(*addon_preferences.prefs_base, 1.0)
    normal=(*addon_preferences.prefs_lamp, 1.0)
    meshnormal=(*addon_preferences.prefs_meshlight, 1.0)
    border=(*addon_preferences.prefs_border, 1.0)
    multsp=space/10
    multsi=size/10
    chks=0
    
    #create lamp lists
    if lampIO==True:
        if layer==False:
            for n in bpy.context.scene.objects:
                if n.type=='LAMP':
                    if n.select==True:
                        chks=1
                    lights.append(n.name)
                    lamps.append(n.name)
                    new2dCo = location_3d_to_region_2d(context.region, \
                                               context.space_data.region_3d, \
                                               n.location)
                    try:
                        location.append([new2dCo.x,new2dCo.y])
                    except AttributeError:
                        pass
                    if n.hide_render==False :
                        isolated.append(n.name)
                        new2dCo = location_3d_to_region_2d(context.region, \
                                               context.space_data.region_3d, \
                                               n.location)
                        try:
                            oklocation.append([new2dCo.x,new2dCo.y])
                        except AttributeError:
                            pass
                    else:
                        hidden.append(n.name)
                    if n.hide==True:
                        notvisible.append(n.name)
        else:
            scene=bpy.context.scene
            slayers=[i for i in range(len(scene.layers)) if scene.layers[i] == True]
            for n in scene.objects:
                if n.type=='LAMP':
                    if n.select==True:
                        chks=1
                    for i in range(len(n.layers)):
                        if n.layers[i] == True and i in slayers:
                            lights.append(n.name)
                            lamps.append(n.name)
                            new2dCo = location_3d_to_region_2d(context.region, \
                                                       context.space_data.region_3d, \
                                                       n.location)
                            try:
                                location.append([new2dCo.x,new2dCo.y])
                            except AttributeError:
                                pass
                            if n.hide_render==False :
                                isolated.append(n.name)
                                new2dCo = location_3d_to_region_2d(context.region, \
                                                       context.space_data.region_3d, \
                                                       n.location)
                                try:
                                    oklocation.append([new2dCo.x,new2dCo.y])
                                except AttributeError:
                                    pass
                            else:
                                hidden.append(n.name)
                            if n.hide==True:
                                notvisible.append(n.name)
                                
    #create meshlights lists
    if meshIO==True:
        if layer==False:
            for n in bpy.context.scene.objects:
                if n.type=='MESH' and n.active_material is not None and n.active_material.use_nodes==True:
                    chkm=0
                    for node in n.active_material.node_tree.nodes:
                        if node.type=='EMISSION' and node.mute==False and node.outputs[0].is_linked==True:
                            chkm=1
                    if chkm==1:
                        if n.select==True:
                            chks=1
                        mesh.append(n.name)
                        lamps.append(n.name)
                        new2dCo = location_3d_to_region_2d(context.region, \
                                                   context.space_data.region_3d, \
                                                   n.location)
                        try:
                            location.append([new2dCo.x,new2dCo.y])
                        except AttributeError:
                            pass
                        if n.hide_render==False :
                            meshisolated.append(n.name)
                            new2dCo = location_3d_to_region_2d(context.region, \
                                                   context.space_data.region_3d, \
                                                   n.location)
                            try:
                                meshoklocation.append([new2dCo.x,new2dCo.y])
                            except AttributeError:
                                pass
                        else:
                            meshhidden.append(n.name)
                        if n.hide==True:
                            meshnotvisible.append(n.name)
        else:
            scene=bpy.context.scene
            slayers=[i for i in range(len(scene.layers)) if scene.layers[i] == True]
            for n in bpy.context.scene.objects:
                if n.type=='MESH' and n.active_material is not None and n.active_material.use_nodes==True:
                    chkm=0
                    for node in n.active_material.node_tree.nodes:
                        if node.type=='EMISSION' and node.mute==False and node.outputs[0].is_linked==True:
                            chkm=1
                    if chkm==1:
                        if n.select==True:
                            chks=1
                        for i in range(len(n.layers)):
                            if n.layers[i] == True and i in slayers:
                                mesh.append(n.name)
                                lamps.append(n.name)
                                new2dCo = location_3d_to_region_2d(context.region, \
                                                           context.space_data.region_3d, \
                                                           n.location)
                                try:
                                    location.append([new2dCo.x,new2dCo.y])
                                except AttributeError:
                                    pass
                                if n.hide_render==False :
                                    meshisolated.append(n.name)
                                    new2dCo = location_3d_to_region_2d(context.region, \
                                                           context.space_data.region_3d, \
                                                           n.location)
                                    try:
                                        meshoklocation.append([new2dCo.x,new2dCo.y])
                                    except AttributeError:
                                        pass
                                else:
                                    meshhidden.append(n.name)
                                if n.hide==True:
                                    meshnotvisible.append(n.name)
            
    # screen lamps
        
    font_id = 0
    #base=int(60*multsp)
    base=60
    if lampIO==True:
        if mx<15 or mx>int(150*multsi) or my<base+20:
            self.hover2=''
        if winman.isolatelight_unrendered_modal==True:
            if len(hidden)!=0:
                for n in hidden:
                    chk=0
                    base+=int(20*multsp)
                    blf.position(font_id, 15, base, 0)
                    blf.size(font_id, int(15*(size/10)), 72)
                    if mx>15 and mx<int(40*multsi) and my>base and my<=base+20:
                        bgl.glColor4f(*surlign)
                        for n2 in lights:
                            if n==n2:
                                hover=lamps.index(n2)
                                self.hover2="R'''"+n2
                    else:
                        bgl.glColor4f(*wh)
                    blf.draw(font_id, "[U]")
                    
                    blf.position(font_id, int(40*multsi), base, 0)
                    if mx>=int(40*multsi) and mx<int(65*multsi) and my>base and my<=base+20:
                        bgl.glColor4f(*surlign)
                        for n2 in lights:
                            if n==n2:
                                hover=lamps.index(n2)
                                self.hover2="V'''"+n2
                    else:
                        bgl.glColor4f(*wh)
                    for n2 in notvisible:
                        if n2==n:
                            chk=1
                    if chk==1:
                        blf.draw(font_id, "[H]")
                    else:
                        blf.draw(font_id, "[V]")
                    
                    blf.position(font_id, int(65*multsi), base, 0)
                    if mx>=int(65*multsi) and mx<int(150*multsi) and my>base and my<=base+20:
                        bgl.glColor4f(*surlign)
                        for n2 in lights:
                            if n==n2:
                                hover=lamps.index(n2)
                                self.hover2=n2
                    else:
                        bgl.glColor4f(*wh)
                    blf.draw(font_id, n)
                        
                if my>base+20:
                    self.hover2=''
        if len(hidden)!=0 and len(isolated)!=0 and winman.isolatelight_unrendered_modal==True:
            base+=int(20*multsp)
            bgl.glLineWidth(2)
            bgl.glColor4f(*wh)
            bgl.glBegin(bgl.GL_LINE_STRIP)
            bgl.glVertex2f(15, base)
            bgl.glVertex2f(100, base)
            bgl.glEnd()

            base-=int(10*multsp)
        if len(isolated)!=0:
            for n in isolated:
                chk=0
                base+=int(20*multsp)
                blf.position(font_id, 15, base, 0)
                blf.size(font_id, int(15*(size/10)), 72)
                if mx>15 and mx<int(40*multsi) and my>base and my<=base+20:
                    bgl.glColor4f(*surlign)
                    for n2 in lights:
                        if n==n2:
                            hover=lamps.index(n2)
                            self.hover2="R'''"+n2
                else:
                    bgl.glColor4f(*wh)
                blf.draw(font_id, "[R]")
                    
                blf.position(font_id, int(40*multsi), base, 0)
                if mx>=int(40*multsi) and mx<int(65*multsi) and my>base and my<=base+20:
                    bgl.glColor4f(*surlign)
                    for n2 in lights:
                        if n==n2:
                            hover=lamps.index(n2)
                            self.hover2="V'''"+n2
                else:
                    bgl.glColor4f(*wh)
                for n2 in notvisible:
                    if n2==n:
                        chk=1
                if chk==1:
                    blf.draw(font_id, "[H]")
                else:
                    blf.draw(font_id, "[V]")
                    
                blf.position(font_id, int(65*multsi), base, 0)
                if mx>=int(65*multsi) and mx<int(150*multsi) and my>base and my<=base+20:
                    bgl.glColor4f(*surlign)
                    for n2 in lights:
                        if n==n2:
                            hover=lamps.index(n2)
                            self.hover2=n2
                else:
                    bgl.glColor4f(*wh)
                blf.draw(font_id, n)
                    
            if my>base+20:
                self.hover2=''
        
        if len(hidden)!=0 and winman.isolatelight_unrendered_modal==True or len(isolated)!=0:
            bgl.glColor4f(*wh)
            base+=int(23*multsp)
            blf.position(font_id, 15, base, 0)
            blf.size(font_id, int(13*(size/10)), 72)
            blf.draw(font_id, "Lamps")
            base+=int(20*multsp)
            
    # screen meshlights
    if meshIO==True:
#        if mx<15 or mx>int(150*multsi) or my<base+20:
#            self.hover2=''
        if winman.isolatelight_unrendered_modal==True:
            if len(meshhidden)!=0:
                for n in meshhidden:
                    chk=0
                    base+=int(20*multsp)
                    blf.position(font_id, 15, base, 0)
                    blf.size(font_id, int(15*(size/10)), 72)
                    if mx>15 and mx<int(40*multsi) and my>base and my<=base+20:
                        bgl.glColor4f(*surlign)
                        for n2 in mesh:
                            if n==n2:
                                hover=lamps.index(n2)
                                self.hover2="R'''"+n2
                    else:
                        bgl.glColor4f(*wh)
                    blf.draw(font_id, "[U]")
                    
                    blf.position(font_id, int(40*multsi), base, 0)
                    if mx>=int(40*multsi) and mx<int(65*multsi) and my>base and my<=base+20:
                        bgl.glColor4f(*surlign)
                        for n2 in mesh:
                            if n==n2:
                                hover=lamps.index(n2)
                                self.hover2="V'''"+n2
                    else:
                        bgl.glColor4f(*wh)
                    for n2 in meshnotvisible:
                        if n2==n:
                            chk=1
                    if chk==1:
                        blf.draw(font_id, "[H]")
                    else:
                        blf.draw(font_id, "[V]")
                    
                    blf.position(font_id, int(65*multsi), base, 0)
                    if mx>=int(65*multsi) and mx<int(150*multsi) and my>base and my<=base+20:
                        bgl.glColor4f(*surlign)
                        for n2 in mesh:
                            if n==n2:
                                hover=lamps.index(n2)
                                self.hover2=n2
                    else:
                        bgl.glColor4f(*wh)
                    blf.draw(font_id, n)
                        
                if my>base+20:
                    self.hover2=''
        if len(meshhidden)!=0 and len(meshisolated)!=0 and winman.isolatelight_unrendered_modal==True:
            base+=int(20*multsp)
            bgl.glLineWidth(2)
            bgl.glColor4f(*wh)
            bgl.glBegin(bgl.GL_LINE_STRIP)
            bgl.glVertex2f(15, base)
            bgl.glVertex2f(100, base)
            bgl.glEnd()

            base-=int(10*multsp)
        if len(meshisolated)!=0:
            for n in meshisolated:
                chk=0
                base+=int(20*multsp)
                blf.position(font_id, 15, base, 0)
                blf.size(font_id, int(15*(size/10)), 72)
                if mx>15 and mx<int(40*multsi) and my>base and my<=base+20:
                    bgl.glColor4f(*surlign)
                    for n2 in mesh:
                        if n==n2:
                            hover=lamps.index(n2)
                            self.hover2="R'''"+n2
                else:
                    bgl.glColor4f(*wh)
                blf.draw(font_id, "[R]")
                    
                blf.position(font_id, int(40*multsi), base, 0)
                if mx>=int(40*multsi) and mx<int(65*multsi) and my>base and my<=base+20:
                    bgl.glColor4f(*surlign)
                    for n2 in mesh:
                        if n==n2:
                            hover=lamps.index(n2)
                            self.hover2="V'''"+n2
                else:
                    bgl.glColor4f(*wh)
                for n2 in notvisible:
                    if n2==n:
                        chk=1
                if chk==1:
                    blf.draw(font_id, "[H]")
                else:
                    blf.draw(font_id, "[V]")
                    
                blf.position(font_id, int(65*multsi), base, 0)
                if mx>=int(65*multsi) and mx<int(150*multsi) and my>base and my<=base+20:
                    bgl.glColor4f(*surlign)
                    for n2 in mesh:
                        if n==n2:
                            hover=lamps.index(n2)
                            self.hover2=n2
                else:
                    bgl.glColor4f(*wh)
                blf.draw(font_id, n)
                    
            if my>base+20:
                self.hover2=''
        
        if len(meshhidden)!=0 and winman.isolatelight_unrendered_modal==True or len(meshisolated)!=0:
            bgl.glColor4f(*wh)
            base+=int(23*multsp)
            blf.position(font_id, 15, base, 0)
            blf.size(font_id, int(13*(size/10)), 72)
            blf.draw(font_id, "MeshLights")
                
    if chks==1:
        base+=int(40*multsp)
        blf.position(font_id, 15, base, 0)
        blf.size(font_id, int(20*(size/10)), 72)
        if mx>15 and mx<int(150*multsi) and my>base and my<=base+20:
            bgl.glColor4f(*surlign)
            self.hover2='isolate'
        else:
            bgl.glColor4f(*wh)
        if winman.isolatelight_on_off==True:
            blf.draw(font_id, "De Isolate")
        else:
            blf.draw(font_id, "Isolate")
        
    if my>base+20:
        self.hover2=''
        
    if layer==True:
        bgl.glColor4f(*wh)
        base+=int(25*multsp)
        blf.position(font_id, 15, base, 0)
        blf.size(font_id, int(13*(size/10)), 72)
        blf.draw(font_id, "Active Layers Only")
    
    if winman.isolatelight_help_modal==True:
        bgl.glColor4f(*wh)
        base+=int(40*multsp)
        blf.position(font_id, 15, base, 0)
        blf.size(font_id, int(13*(size/10)), 72)
        blf.draw(font_id, "Esc to Quit")
        
        base+=int(20*multsp)
        blf.position(font_id, 15, base, 0)
        blf.size(font_id, int(13*(size/10)), 72)
        blf.draw(font_id, "Ctrl + Shift + Left Click to Add lamp to selection")
                
        base+=int(20*multsp)
        blf.position(font_id, 15, base, 0)
        blf.size(font_id, int(13*(size/10)), 72)
        blf.draw(font_id, "Ctrl + Left Click to Interact")
        
        base+=int(20*multsp)
        blf.position(font_id, 15, base, 0)
        blf.size(font_id, int(13*(size/10)), 72)
        blf.draw(font_id, "[U] - Unrendered")        
        
        base+=int(20*multsp)
        blf.position(font_id, 15, base, 0)
        blf.size(font_id, int(13*(size/10)), 72)
        blf.draw(font_id, "[R] - Rendered")
        
        base+=int(20*multsp)
        blf.position(font_id, 15, base, 0)
        blf.size(font_id, int(13*(size/10)), 72)
        blf.draw(font_id, "[H] - Hidden")
                
        base+=int(20*multsp)
        blf.position(font_id, 15, base, 0)
        blf.size(font_id, int(13*(size/10)), 72)
        blf.draw(font_id, "[V] - Visible")
            
    if lampIO==True or meshIO==True:
        # 50% alpha, 2 pixel width line
        bgl.glEnable(bgl.GL_BLEND)
        bgl.glColor4f(*normal)
        lw = 4 // 2
        bgl.glLineWidth(lw*2)

        bgl.glLineWidth(lw)
        l=15
        if lampIO==True:
            for n in oklocation:
                bgl.glColor4f(*normal)
                bgl.glBegin(bgl.GL_LINE_STRIP)
                x=n[0]
                y=n[1]
                #for x, y in location:
                bgl.glVertex2f(x-l, y+l)
                bgl.glVertex2f(x-l, y-l)
                bgl.glVertex2f(x+l, y-l)
                bgl.glVertex2f(x+l, y+l)
                bgl.glVertex2f(x-l, y+l)
                bgl.glEnd()
        if meshIO==True:
            for n in meshoklocation:
                bgl.glColor4f(*meshnormal)
                bgl.glBegin(bgl.GL_LINE_STRIP)
                x=n[0]
                y=n[1]
                #for x, y in location:
                bgl.glVertex2f(x-l, y+l)
                bgl.glVertex2f(x-l, y-l)
                bgl.glVertex2f(x+l, y-l)
                bgl.glVertex2f(x+l, y+l)
                bgl.glVertex2f(x-l, y+l)
                bgl.glEnd()
        if self.hover2!='' and self.hover2!='isolate':
            for n in location:
                if hover==location.index(n):
                    bgl.glColor4f(*surlign)
                    bgl.glBegin(bgl.GL_LINE_STRIP)
                    x=n[0]
                    y=n[1]
                    #for x, y in location:
                    bgl.glVertex2f(x-l, y+l)
                    bgl.glVertex2f(x-l, y-l)
                    bgl.glVertex2f(x+l, y-l)
                    bgl.glVertex2f(x+l, y+l)
                    bgl.glVertex2f(x-l, y+l)
                    bgl.glEnd()
   
                    
    # draw outline of screen
    bgl.glEnable(bgl.GL_BLEND)
    bgl.glColor4f(*border)
    lw = 4 // 2
    bgl.glLineWidth(lw*2)

    r = context.region

    bgl.glBegin(bgl.GL_LINE_STRIP)
    bgl.glVertex2i(lw, lw)
    bgl.glVertex2i(r.width - lw, lw)
    bgl.glVertex2i(r.width - lw, r.height - lw)
    bgl.glVertex2i(lw, r.height - lw)
    bgl.glVertex2i(lw, lw)
    bgl.glEnd()

class IsolateLightModalDraw(bpy.types.Operator):
    bl_idname = "isolatelight.modaldraw"
    bl_label = "Overlay Lights Informations"
    bl_description = "Activate Viewport Lamp Helper - Esc to quit"
    
    hover2 = bpy.props.StringProperty()
    _timer = None
    
    @classmethod
    def poll(cls, context):
        working=bpy.data.window_managers['WinMan'].isolatelight_modal_working
        return working==False
    
    def __init__(self):
        bpy.data.window_managers['WinMan'].isolatelight_modal_working=True
    
    def modal(self, context, event):
        try:
            for area in context.screen.areas:
                if area.type == 'VIEW_3D':
                    area.tag_redraw()
        except AttributeError:
            pass
        onoff=bpy.data.window_managers['WinMan'].isolatelight_on_off
        winman=bpy.data.window_managers['WinMan']
                
        if event.type == 'MOUSEMOVE':
            if event.mouse_region_x is not None:
                winman.isolatelight_mx=event.mouse_region_x
            if event.mouse_region_y is not None:
                winman.isolatelight_my=event.mouse_region_y
            return {'PASS_THROUGH'}
        
        if  event.type == 'LEFTMOUSE' and event.ctrl==True and event.shift==True:
            print('test')
            if self.hover2!='':
                for ob in bpy.context.scene.objects:
                    if ob.name==self.hover2:
                        ob.select=True
                        bpy.context.scene.objects.active = ob
                
        if event.type == 'LEFTMOUSE' and event.ctrl==True and event.alt==False and event.shift==False:
            if self.hover2!='':
                if self.hover2=='isolate':
                    if winman.isolatelight_on_off==True:
                        bpy.ops.isolatelight.deisolate_light()
                    else:
                        bpy.ops.isolatelight.isolate_light()
                elif "R'''" in self.hover2:
                    for ob in bpy.context.scene.objects:
                        if ob.name==self.hover2.split("'''")[1]:
                            ob.hide_render = not ob.hide_render
                elif "V'''" in self.hover2:
                    for ob in bpy.context.scene.objects:
                        if ob.name==self.hover2.split("'''")[1]:
                            ob.hide = not ob.hide
                else:
                    for ob in bpy.context.scene.objects:
                        ob.select=False
                        if ob.name==self.hover2:
                            ob.select=True
                            bpy.context.scene.objects.active = ob
        
        if event.type =='ESC':
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            bpy.data.window_managers['WinMan'].isolatelight_modal_working=False 
            return {'CANCELLED'}

        if event.type == 'TIMER':
            return {'PASS_THROUGH'}
                
        return {'PASS_THROUGH'}
        
    def execute(self, context):
        if context.area.type == 'VIEW_3D':
            wm = context.window_manager
            # the arguments we pass the the callback
            args = (self, context)
            # Add the region OpenGL drawing callback
            # draw in view space with 'POST_VIEW' and 'PRE_VIEW'
            self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_light, args, 'WINDOW', 'POST_PIXEL')
            self._timer = wm.event_timer_add(0.1, context.window)
            wm.modal_handler_add(self)
            self.mouse_x=0
            self.mouse_y=0
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)

        

# isolate
class Isolateligth_Isolate(bpy.types.Operator):
    bl_idname = "isolatelight.isolate_light"
    bl_label = "Isolate selected light"
    bl_description = "Isolate selected light"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        winman=bpy.data.window_managers['WinMan']
        scene=bpy.context.scene
        active=bpy.context.active_object
        dupelist=[]

        chk=0
        for ob in bpy.context.scene.objects:
            if ob.type=='LAMP':
                chkm=1
            elif ob.type=='MESH' and ob.active_material is not None and ob.active_material.use_nodes==True:
                chkm=0
                for node in ob.active_material.node_tree.nodes:
                    if node.type=='EMISSION' and node.mute==False and node.outputs[0].is_linked==True:
                        chkm=1
            if chkm==1 and ob.select==True:
                chk=1
                    
        if chk==1:
            if winman.isolatelight_on_off==False:
                for ob in bpy.context.scene.objects:
                    if ob.type=='LAMP':
                        chk=0
                        for n in dupelist:
                            if n==ob.name:
                                chk=1
                        if chk==0:
                            bpy.data.window_managers['WinMan'].isolatelight_old_light=bpy.data.window_managers['WinMan'].isolatelight_old_light+str(ob.name)+"'''"+str(ob.hide)+"'''"+str(ob.hide_render)+"____"
                            dupelist.append(ob.name)
                        if ob.select==False:
                            if winman.isolatelight_only_render==False:
                                ob.hide=True
                            ob.hide_render=True
                        else:
                            ob.hide=False
                            ob.hide_render=False
                    elif ob.type=='MESH' and ob.active_material is not None and ob.active_material.use_nodes==True:
                        chkm=0
                        for node in ob.active_material.node_tree.nodes:
                            if node.type=='EMISSION' and node.mute==False and node.outputs[0].is_linked==True:
                                chkm=1
                        if chkm==1:
                            chk=0
                            for n in dupelist:
                                if n==ob.name:
                                    chk=1
                            if chk==0:
                                bpy.data.window_managers['WinMan'].isolatelight_old_light=bpy.data.window_managers['WinMan'].isolatelight_old_light+str(ob.name)+"'''"+str(ob.hide)+"'''"+str(ob.hide_render)+"____"
                                dupelist.append(ob.name)
                            if ob.select==False:
                                if winman.isolatelight_only_render==False:
                                    ob.hide=True
                                ob.hide_render=True
                            else:
                                ob.hide=False
                                ob.hide_render=False
                winman.isolatelight_on_off=True
            else:
                self.report({'WARNING'}, "Light(s) already Isolated")
        else:
            self.report({'WARNING'}, "Please Select Light(s)")
                                
        return {'FINISHED'}
    
# de isolate
class Isolateligth_DeIsolate(bpy.types.Operator):
    bl_idname = "isolatelight.deisolate_light"  
    bl_label = "De Isolate selected light"
    bl_description = "De Isolate selected light"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        winman=bpy.data.window_managers['WinMan']
        scene=bpy.context.scene
        active=bpy.context.active_object
        
        if winman.isolatelight_on_off==True:
            winman.isolatelight_on_off=False
            if winman.isolatelight_old_light!="____" and winman.isolatelight_old_light!="":
                for n in str(winman.isolatelight_old_light).split("____"):
                    for ob in bpy.context.scene.objects:
                        if n.split("'''")[0]==ob.name:
                            if n.split("'''")[1]=="True":
                                ob.hide=True
                            else:
                                ob.hide=False
                            if n.split("'''")[2]=="True":
                                ob.hide_render=True
                            else:
                                ob.hide_render=False
                winman.isolatelight_old_light='____'
            else:
                self.report({'WARNING'}, "No Isolated Light(s)")
        else:
            self.report({'WARNING'}, "No Isolated Light(s)")
        return {'FINISHED'}
        
    
#draw in header
def isolate_menu_draw(self, context):
    winman=bpy.data.window_managers['WinMan']
    active_ob=context.active_object
    chk=0
    layout = self.layout
    row=layout.row(align=True)
    for ob in context.scene.objects:
        chkm=0
        if ob.type=='LAMP':
            chkm=1
        elif ob.type=='MESH' and ob.active_material is not None and ob.active_material.use_nodes==True:
            chkm=0
            for node in ob.active_material.node_tree.nodes:
                if node.type=='EMISSION' and node.mute==False and node.outputs[0].is_linked==True:
                    chkm=1
        if chkm==1 and ob.select==True:
            chk=1
    if chk==1 and winman.isolatelight_on_off==False:
            row.operator('isolatelight.isolate_light', text='', icon='OUTLINER_DATA_LAMP')
            row.prop(winman, 'isolatelight_only_render', text='', icon='RESTRICT_RENDER_OFF')
    elif winman.isolatelight_on_off==True:
        row.operator('isolatelight.deisolate_light', text='', icon='OUTLINER_OB_LAMP')
    row.operator('isolatelight.modaldraw', text='', icon='COLOR')
    if winman.isolatelight_modal_working==True:
        row.separator()
        row.prop(winman, 'isolatelight_lamp_onoff_modal', text='', icon='LAMP_SPOT')
        row.prop(winman, 'isolatelight_meshlight_onoff_modal', text='', icon='MESH_ICOSPHERE')
        row.prop(winman, 'isolatelight_layer_modal', text='', icon='RENDERLAYERS')
        row.prop(winman, 'isolatelight_unrendered_modal', text='', icon='RENDER_REGION')
        row.prop(winman, 'isolatelight_help_modal', text='', icon='QUESTION')
        col=row.column()
        row2=col.row(align=True)
        row2.scale_x = 0.5
        row2.prop(winman, 'isolatelight_font_size', text='')
        row2.prop(winman, 'isolatelight_font_space', text='')
          
                    
def register():
    bpy.utils.register_class(IsolateLightAddonPrefs)
    bpy.utils.register_class(Isolateligth_Isolate)
    bpy.utils.register_class(Isolateligth_DeIsolate)
    bpy.utils.register_class(IsolateLightModalDraw)
    
    bpy.types.WindowManager.isolatelight_old_light = bpy.props.StringProperty(default="____")
    bpy.types.WindowManager.isolatelight_on_off = bpy.props.BoolProperty(default=False)
    bpy.types.WindowManager.isolatelight_only_render = bpy.props.BoolProperty(default=False, description="If Enabled, unselected Lamps will be only hide for render when Isolating")
    bpy.types.WindowManager.isolatelight_mx = bpy.props.IntProperty()
    bpy.types.WindowManager.isolatelight_my = bpy.props.IntProperty()
    bpy.types.WindowManager.isolatelight_font_size = bpy.props.IntProperty(min=1, max=30, default=10, description="Font Size on the Viewport GUI")
    bpy.types.WindowManager.isolatelight_font_space = bpy.props.IntProperty(min=1, max=30, default=10, description="Font Space on the Viewport GUI")
    bpy.types.WindowManager.isolatelight_help_modal = bpy.props.BoolProperty(default=False, description="Display Help on the Viewport GUI")
    bpy.types.WindowManager.isolatelight_unrendered_modal = bpy.props.BoolProperty(default=True, description="Display only Rendered Elements on the Viewport GUI")
    bpy.types.WindowManager.isolatelight_layer_modal = bpy.props.BoolProperty(default=True, description="If Enabled, only Elements on active layers will be displayed")
    bpy.types.WindowManager.isolatelight_lamp_onoff_modal = bpy.props.BoolProperty(default=True, description="If Enabled, Lamps will be displayed")
    bpy.types.WindowManager.isolatelight_meshlight_onoff_modal = bpy.props.BoolProperty(default=True, description="If Enabled, MeshLights will be displayed")
    bpy.types.WindowManager.isolatelight_modal_working = bpy.props.BoolProperty(default=False)
    
    bpy.types.VIEW3D_HT_header.append(isolate_menu_draw)
        
def unregister():
    bpy.utils.unregister_class(IsolateLightAddonPrefs)
    bpy.utils.unregister_class(Isolateligth_Isolate)
    bpy.utils.unregister_class(Isolateligth_DeIsolate)
    bpy.utils.unregister_class(IsolateLightModalDraw)
    
    del bpy.types.WindowManager.isolatelight_old_light
    del bpy.types.WindowManager.isolatelight_on_off
    del bpy.types.WindowManager.isolatelight_only_render
    del bpy.types.WindowManager.isolatelight_mx
    del bpy.types.WindowManager.isolatelight_my
    del bpy.types.WindowManager.isolatelight_font_size
    del bpy.types.WindowManager.isolatelight_font_space
    del bpy.types.WindowManager.isolatelight_modal_working
    
    bpy.types.VIEW3D_HT_header.remove(isolate_menu_draw)
    
if __name__ == "__main__":
    register()