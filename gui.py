# -*- coding: utf-8 -*-

import urwid, time
from collections import OrderedDict


PALETTE = [("top","white","black"),
               ("line","white","dark green","standout"),
               ("line_eq","black","light gray","standout"),
               ("frame","white","white"),
               ("reversed", "standout", ""),
               ("common","white",""),
               ("uncommon","light blue",""),
               ("rare","yellow",""),
               ("unique","light magenta",""),
               ("set","light green",""),
               ("red", "dark red", ""),
               ("yellow", "yellow", ""),
               ("blue", "light blue", "")
               ]

class GUI(object):

    def __init__(self, master):
        self.master = master
        self.game_screen = GameScreen(master)
        self.start_screen = StartScreen(master)
        self.create_screen = CreateScreen(master)
        self.load_screen = None
        self.help_screen = HelpScreen(master)
        
        self.main = urwid.Padding(self.start_screen, left=2, right=2)#main screen, change it to any screen you need with self.main.original_widget
        self.top = urwid.Overlay(self.main, urwid.SolidFill(u"\N{LIGHT SHADE}"),
            align="center", width=("relative", 60),
            valign="middle", height=("relative", 60),
            min_width=120, min_height=60)
            
        self.loop = urwid.MainLoop(self.top, PALETTE, unhandled_input=self.game_screen.handle_input)
        
    def to_game_screen(self):
        self.main.original_widget = self.game_screen 
    def to_create_screen(self):
        self.main.original_widget = self.create_screen
    def to_load_screen(self):
        self.main.original_widget = self.load_screen
    def to_help_screen(self):
        self.main.original_widget = self.help_screen
        
        
class StartScreen(urwid.Overlay):
    def __init__(self, master):
        self.master = master
        body = [urwid.Divider()]
        new_game_button = urwid.Button("New Game")
        new_game_button._label.align = "center"
        urwid.connect_signal(new_game_button, "click", self.new_game)
        body.append(urwid.AttrMap(new_game_button, None, focus_map="line"))
        quick_game_button = urwid.Button("Quick Start")
        quick_game_button._label.align = "center"
        urwid.connect_signal(quick_game_button, "click", self.quick_game)
        body.append(urwid.AttrMap(quick_game_button, None, focus_map="line"))
        help_button = urwid.Button("Help")
        help_button._label.align = "center"
        urwid.connect_signal(help_button, "click", self.help)
        body.append(urwid.AttrMap(help_button, None, focus_map="line"))
        quit_button = urwid.Button("Quit")
        quit_button._label.align = "center"
        urwid.connect_signal(quit_button, "click", self.exit_program)
        body.append(urwid.AttrMap(quit_button, None, focus_map="line"))
        
        listbox = urwid.ListBox(urwid.SimpleFocusListWalker(body))
        super(StartScreen, self).__init__(listbox, urwid.SolidFill(u"\N{MEDIUM SHADE}"),
            align="center", width=("relative", 60),
            valign="middle", height=("relative", 60),
            min_width=40, min_height=16)     
     
    def new_game(self, button):
        self.master.new_game()
        
    def quick_game(self, button):
        self.master.quick_game()
            
    def help(self, button):
        self.master.gui.to_help_screen()       
    def exit_program(self, button):
        raise urwid.ExitMainLoop()  
        
        
class CreateScreen(urwid.Overlay):
    def __init__(self, master):
        self.master = master
        #list: base value, min value, max value, increment, cost
        self.temp_chars = OrderedDict([("HP", [8, 4, 12, 2, 1]), ("BTH", [6, 4, 18, 1, 1]), ("STR", [6, 4, 18, 1, 1]), ("RES", [6, 4, 18, 1, 1]), 
        ("DEX", [6, 4, 18, 1, 1]), ("MAG", [6, 4, 18, 1, 1])])
        self.temp_text = {key: urwid.Text(str(self.temp_chars[key][0])) for key in self.temp_chars }
        self.points = 40
        self.points_text = urwid.Text("Points: {}".format(self.points))
        self.name_edit = urwid.Edit("Name: ")
        body = [urwid.Text("Create a new character"), urwid.Divider(), self.name_edit, self.points_text]
        
        
        for c in self.temp_chars:
            b_plus = urwid.Button("+")
            urwid.connect_signal(b_plus, "click", self.update_char, user_args = [c, +1])
            b_minus = urwid.Button("-")
            urwid.connect_signal(b_minus, "click", self.update_char, user_args = [c, -1])
            
            
            columns = [(3, urwid.Text(c)), (2, self.temp_text[c]), (1, urwid.AttrMap(b_minus, None, focus_map="line")), (1, urwid.AttrMap(b_plus, None, focus_map="line"))]
            
            line = urwid.Columns(columns, dividechars=1, focus_column=3, min_width=1, box_columns=None)
            body.append(line)
        
        body.append(urwid.Divider())
        
        start_button = urwid.Button("Start")
        start_button._label.align = "center"
        urwid.connect_signal(start_button, "click", self.start)
        body.append(urwid.AttrMap(start_button, None, focus_map="line"))
        back_button = urwid.Button("Back")
        back_button._label.align = "center"
        urwid.connect_signal(back_button, "click", self.back)
        body.append(urwid.AttrMap(back_button, None, focus_map="line"))
        listbox = urwid.ListBox(urwid.SimpleFocusListWalker(body))
        super(CreateScreen, self).__init__(listbox, urwid.SolidFill(u"\N{MEDIUM SHADE}"),
            align="center", width=("relative", 60),
            valign="middle", height=("relative", 60),
            min_width=40, min_height=16)   
            
     
    def update_char(self, char, value, button):
        if (self.temp_chars[char][2]>=self.temp_chars[char][0] + value * self.temp_chars[char][3]>= self.temp_chars[char][1]) and self.points - value * self.temp_chars[char][4]>=0:
            self.points -= value * self.temp_chars[char][4]
            self.temp_chars[char][0] += value * self.temp_chars[char][3]
            self.temp_text[char].set_text(str(self.temp_chars[char][0]))
            self.points_text.set_text("Points: {}".format(self.points))
    def start(self, button):
        self.master.create_player(self.name_edit.get_edit_text()[:11], {key: self.temp_chars[key][0] for key in self.temp_chars })
        
    def back(self, button):
        self.master.gui.main.original_widget = self.master.gui.start_screen
        
class HelpScreen(urwid.Overlay):
    def __init__(self, master):
        self.master = master
        
        text = """
write me, help!
help!
        
"""
        utext = urwid.Text(text)
        
        body = [utext]
       
        back_button = urwid.Button("Back")
        back_button._label.align = "center"
        urwid.connect_signal(back_button, "click", self.back)
        body.append(urwid.AttrMap(back_button, None, focus_map="line"))
        listbox = urwid.ListBox(urwid.SimpleFocusListWalker(body))
        super(HelpScreen, self).__init__(listbox, urwid.SolidFill(u"\N{MEDIUM SHADE}"),
            align="center", width=("relative", 60),
            valign="middle", height=("relative", 60),
            min_width=40, min_height=16)   
            
     
    def back(self, button):
        self.master.gui.main.original_widget = self.master.gui.start_screen           
    
    
class GameScreen(urwid.Frame):
    def __init__(self, master):
        self.master = master
        length = 30
        self.breath_bars_length = max(3, int(0.5 * length))
        self.hp_bars_length = max(3, int(0.5 * length))
        
        widgets = [urwid.AttrMap(widget,None,"line") for widget in [ urwid.Text("")] ]
        self.players_widget = SelectableListBox(urwid.SimpleListWalker(widgets))
        
        
        
        
        
        self.screens = []   
        screens = ("Status", "Inventory", "Equipment", "Location", "Mission")
        labels = []
        for b in screens:
            try:
                self.screens.append({"title" : b, "widget" : SelectableListBox(urwid.SimpleListWalker(widgets)), "state" : "normal", "index" : 1, "callback" : getattr(self, "refresh_{}_widget".format(b.lower()))})
            except:
                continue
            l = urwid.Text("{:^10}".format(b), align="center")
            
            #urwid.connect_signal(l, "change", self.change_body)
            labels.append(urwid.LineBox(urwid.AttrMap(l, None, focus_map="line")))
        self.buttons_column = SelectableColumns(labels)
        
        self.active_screen = self.screens[0]
        super(GameScreen, self).__init__(urwid.LineBox(self.active_screen["widget"], title=""), urwid.LineBox(urwid.BoxAdapter(self.players_widget, 12), title=""),  self.buttons_column , focus_part="header")
        urwid.AttrMap(self,"frame")
        
        
        
    def handle_input(self, input):
        if input == "esc":
            raise urwid.ExitMainLoop()
        elif input == "down" and self.focus_position == "body":
            self.focus_position = "footer"
        elif input == "up" and self.focus_position == "body":
            self.focus_position = "header"
        elif (input == "up" and self.focus_position == "footer") or (input == "down" and self.focus_position == "header"):
            self.focus_position = "body"
        elif input == "right":
            if self.focus_position == "header":
                self.players_widget.focus_next() 
            elif self.focus_position == "body":
                self.active_screen["widget"].focus_next() 
            elif self.focus_position == "footer":
                self.buttons_column.focus_next() 
        elif input == "left":
            if self.focus_position == "header":
                self.players_widget.focus_previous()
            elif self.focus_position == "body":
                self.active_screen["widget"].focus_previous() 
            elif self.focus_position == "footer":
                self.buttons_column.focus_previous() 
        elif input == "s":
            self.buttons_column.focus_position = 0 
        elif input == "i":
            self.buttons_column.focus_position = 1  
        elif input == "e":
            self.buttons_column.focus_position = 2  
        elif input == "l":
            self.buttons_column.focus_position = 3
        elif input == "m":
            self.buttons_column.focus_position = 4 
        
        elif input in (str(i) for i in xrange(1, 10)):
            try:
                self.players_widget.focus_position = int(input)-1 
            except:
                pass       
        
        elif input == "enter":
            self.master.tire(self.players_widget.focus_position)
    
           
    def update_screen(self, protagonist):
        players = protagonist.players  
        widgets = []
        for p in players:
            widgets += [urwid.AttrMap(urwid.Text(self.print_status(p),wrap='clip'), None, focus_map="line")]
        self.players_widget.body[:] = widgets
        
        index = self.players_widget.focus_position
        
        self.active_screen = self.screens[self.buttons_column.focus_position]
        self.contents["body"] = (urwid.LineBox(self.active_screen["widget"], title=""), None)
        self.contents["header"][0].set_title(protagonist.name)
        self.refresh_active_screen(players[index])
        
        
    def refresh_active_screen(self, player):
        for s in self.screens:
            if self.active_screen == s:
                self.contents["body"][0].set_title(s["title"])

                s["callback"](player)                
            else:
                s["state"] = "normal"
                s["index"] = 1
    
    def print_status(self, char):
        status = []
                #"➶""⚝""✨""⚔"❂✮ ⚝
        if char.is_dead:
            h = u"☠"
        elif char.is_dreaming:
            h = u"☾"
        elif char.is_shocked:
            h = u"⚡"
        elif char.is_muted:
            h = u"∅"
        else: 
            h = [u"♡",u"♥"][int(time.time()*(char.world.generation+1))%2] 
        
        if char.is_catching_breath:        
            breath = "Breathing "            
        elif char.BTH >= 0:
            b = "Breath"
            breath = "{:<6s}:{:<3d}".format(b, char.BTH)

        incipit = char.job.name + " " + str(char.job.level) if char.__class__.__name__ == "Player" else char.name + ' ' + char.race.name
        status.append((None, u"{:12s} {:1s} {:^18s}\n".format(incipit, h, breath)))
        
        hp_bars = int(round(1.*char.HP/char.max_HP  * self.hp_bars_length))
        if 1.*char.HP/char.max_HP <= 0.5:
            status.append(("yellow", u"{:16s} ".format(hp_bars * u"\u25B0" + (self.hp_bars_length - hp_bars) * u"\u25B1")))
        elif 1.*char.HP/char.max_HP <= 0.2:
            status.append(("red", u"{:16s} ".format(hp_bars * u"\u25B0" + (self.hp_bars_length - hp_bars) * u"\u25B1")))
        else:
            status.append(("common",u"{:16s} ".format(hp_bars * u"\u25B0" + (self.hp_bars_length - hp_bars) * u"\u25B1")))

        if char.is_catching_breath:
            breath_bars = int( round((1.-char.is_catching_breath/char.time_to_catch_breath()) * self.breath_bars_length))
            status.append(("blue",u"{:17s} ".format(breath_bars * u"\u25AE" + (self.breath_bars_length - breath_bars) * u"\u25AF")))
        elif char.BTH >= 0:
            breath_bars = int(round(1.*char.BTH/char.max_BTH * self.breath_bars_length))
            status.append(("common",u"{:17s} ".format(breath_bars * u"\u25AE" + (self.breath_bars_length - breath_bars) * u"\u25AF")))
        status.append(("common",u"{:<100s}".format(char.print_action)))

        return status
              
    def refresh_status_widget(self, player):
        def toggle_strategy(button):
            player.toggle_strategy()
        def toggle_auto_loot(button):
            player.auto_loot = not player.auto_loot
        def get_hist(char):
            chars_height = 6
            h = []
            color = ["red", "yellow", "blue"][(char-1)/2]
            for i in xrange(chars_height):
                if char >= chars_height-i:
                    h.append((color, u"\u2592\u2588\u2588 "))
                elif char == chars_height-i-1:
                    h.append((color, u" \u2582\u2582 "))
                else:
                    h.append((color, "    "))

            return h
    
        state = ""
        if player.is_dead:
            state += "Dead "
        if player.is_dreaming:
            state += "Dreaming "
        if player.is_muted:
            state += "Muted "
        if player.is_shocked:
            state += "Shocked "

        data = ["World:{:1d}/{:1d} {:>10s} {:<10s} Lev:{:2d} Exp:{:<6d} {}\n".format(player.generation, player.world.generation, player.race.name, player.job.name, player.level, player.exp, state),
                "BTH:{:>3d}/{:<3d} HP:{:<11s} RTM:{:<3d}\n".format(player.BTH, player.max_BTH, str(player.HP)+"/"+str(player.max_HP), player.on_rythm),
                "Abilities: {}\n".format(" - ".join(["{}: {} ({:<2d}%)".format(ab, player.all_abilities()[ab].name, int(round(player.strategy.priority[ab] * 100./sum([player.strategy.priority[k] for k in player.all_abilities()]),0))) for ab in player.all_abilities()])),
                "Location: {} --> {}\n".format(player.location.name, player.master_location_path.split("/")[-1])]
        chars = []
        
        hist = [get_hist(c) for c in [player.STRmod, player.RESmod, player.MAGmod, player.DEXmod]]
      
        chars = []
        for h in zip(*hist):
            h = list(h)
            h.append("\n")
            chars.append(h)
        chars.append(u"{:^3d} {:^3d} {:^3d} {:^3d} \n".format(player.STRmod, player.RESmod, player.MAGmod, player.DEXmod))
        chars.append(u"STR RES MAG DEX ")
        
        b = urwid.Button("{}".format(player.strategy.name))
        b._label.align = "center"
        urwid.connect_signal(b, "click", toggle_strategy)
        loot_button = urwid.Button("{}".format(player.auto_loot))
        loot_button._label.align = "center"
        urwid.connect_signal(loot_button, "click", toggle_auto_loot)
        line = [(16, urwid.AttrMap(b, None, focus_map="line")), (24, urwid.Text("{} {}".format(player.strategy.alignment, player.strategy.target))),(10, urwid.Text("Auto Loot:")), (12, urwid.AttrMap(loot_button, None, focus_map="line"))]  
        
        columns = SelectableColumns(line, dividechars=2)
        try:
            index = self.active_screen["widget"].focus_position
            columns.focus_position = self.active_screen["widget"].body[:][index].focus_position
        except:
            pass        
        widgets = [urwid.Columns([(60,urwid.Text(data, align='left')), (30, urwid.Text(chars, align='center'))]), columns]
        self.active_screen["widget"].body[:] = widgets
        
    def refresh_location_widget(self, player):
        def dream(button):
            player.protagonist.dream()
        def warp(button):
            player.protagonist.warp()  
        l = player.location
        

        b1 = urwid.Button("Dream Stone")
        b1._label.align = "center"
        if l.dream_stone:
            urwid.connect_signal(b1, "click", dream)
            b1 = urwid.AttrMap(b1, None, focus_map="line")
        b2 = urwid.Button("Dimensional Warp")
        b2._label.align = "center"
        if l.dimensional_warp:
            urwid.connect_signal(b2, "click", warp)
            b2 = urwid.AttrMap(b2, None, focus_map="line")
        button_line = SelectableColumns([(20, b1), (20, b2)], dividechars = 1)
        loots = ["Lootings: "] + [(loot.rarity, "{} ".format(loot.name)) for loot in l.inventory] 
        widgets = [button_line, urwid.Text(loots)]
        try:
            index = self.active_screen["widget"].focus_position
            button_line.focus_position = self.active_screen["widget"].body[:][index].focus_position
        except:
            pass

        villains = [c for c in l.characters if c.__class__.__name__ == "Villain"]
        for v in villains:
            widgets += [urwid.Text(self.print_status(v),wrap='clip')]

        self.active_screen["widget"].body[:] = widgets
    
    def refresh_mission_widget(self, player):
        def show_missions(button):
            self.active_screen["state"] = "show"
            
        def send_mission(mission, button):
            player.protagonist.start_mission(mission)
            self.active_screen["state"] = "normal"
            
            
        widgets = []
        if self.active_screen["state"] == "normal":
            b = urwid.Button("Missions List") 
            b._label.align = 'center'
            w = urwid.AttrMap(b,None,"line")
            urwid.connect_signal(b, "click", show_missions)
            widgets.append(w) 
            
            mission = player.protagonist.mission
            if mission != None:
                description = mission.description
            else:
                description = "No mission selected"
            data = """{}""".format(description)
            widgets.append(urwid.Text(data, align='center') ) 
            
        else:
            missions = [m for key, m in player.protagonist.missions.iteritems() if m.requisites()]
            for m in missions:
                if m.id in player.protagonist.data["mission"]:
                    w = urwid.Text("{}".format(m.name), align="center") 
                    text = urwid.Text("Accomplished")
                    line = [(32, w), text]
                else:
                    b = urwid.Button("{}".format(m.name)) 
                    b._label.align = 'center'
                    text = urwid.Text("{} Exp".format(m.exp))
                    w = urwid.AttrMap(b,None,"line")
                    urwid.connect_signal(b, "click", send_mission, user_args = [m])
                    line = [(32, w), text]
                columns = SelectableColumns(line, dividechars=2)
                widgets.append(columns)
        
        self.active_screen["widget"].body[:] = widgets
        
    def refresh_inventory_widget(self, player):
        def show_item(item, button):
            self.active_screen["state"] = item.id
        
        def back(button):
            self.active_screen["state"] = "normal"
            
        def drop_item(item, button):
            player.drop(item)
            
        def send_equip(item, button):
            if not item.is_equipped:
                player.equip(item)
            
        def send_unequip(item, button):
            if item.is_equipped:
                player.unequip(item)
        
        widgets = []
        items = [i for i in player.inventory]
        if self.active_screen["state"] == "normal":
            for i in items:
                bonus = ",".join([" {}: {} ".format(bns, i.bonus[bns]) for bns in i.bonus if i.bonus[bns]!=0] ) + " " + ",".join([" {}: {} ".format(ab, i.abilities[ab].name) for ab in i.abilities] )
               
                bname = urwid.Button(i.name)
                bname._label.align = 'center'
                name_button = urwid.AttrMap(bname,i.rarity,"line")
                urwid.connect_signal(bname, "click", show_item, user_args = [i])
                if i.is_equipped:
                    bonus_text = urwid.Text(("line_eq", ("{:^36s}".format(bonus))))
                else:
                    bonus_text = urwid.Text(("{:^36s}".format(bonus)))
                bdrop = urwid.Button("Drop") 
                bdrop._label.align = 'center'
                urwid.connect_signal(bdrop, "click", drop_item, user_args = [i])
                if i.is_equipment:
                    if i.requisites(player):
                        if i.is_equipped:
                            bequip = urwid.Button("Unequip") 
                            bequip._label.align = 'center'
                            urwid.connect_signal(bequip, "click", send_unequip, user_args = [i])
                        elif not i.is_equipped:
                            bequip = urwid.Button("Equip") 
                            bequip._label.align = 'center'
                            urwid.connect_signal(bequip, "click", send_equip, user_args = [i])
                    else:
                        bequip = urwid.Button("Not Equipable") 
                        bequip._label.align = 'center'                
                else:
                    bequip = urwid.Button("Use") 
                    bequip._label.align = 'center'     
                line = [(22, name_button), (38, bonus_text), (18, urwid.AttrMap(bequip,None,"line")),(12, urwid.AttrMap(bdrop,None,"line"))]
                columns = SelectableColumns(line, dividechars=2)
                try:
                    index = self.active_screen["widget"].focus_position
                    columns.focus_position = self.active_screen["widget"].body[:][index].focus_position
                except:
                    pass
                
                widgets.append(columns)
        else:
            i = next((it for it in items if it.id == self.active_screen["state"]), None)
            if i == None:
                self.active_screen["state"] = "normal"
            else:
                name = urwid.Text((i.rarity, i.name))
                widgets.append(name)
                widgets.append(urwid.Text("Rarity: {}".format(i.rarity)))
                bonus = ",".join([" {}: {} ".format(bns, i.bonus[bns]) for bns in i.bonus if i.bonus[bns]!=0] ) + " " + ",".join([" {}: {} ".format(ab, i.abilities[ab].name) for ab in i.abilities] )
                bonus_text = urwid.Text(("{}".format(bonus)))
                widgets.append(bonus_text)
                for d in i.description:
                    widgets.append(urwid.Text(d))
                
                bback = urwid.Button("Back")
                bback._label.align = 'center'
                urwid.connect_signal(bback, "click", back)
                bback = urwid.AttrMap(bback, None, "line")
                
                widgets.append(SelectableColumns([(8, bback)]))       
        self.active_screen["widget"].body[:] = widgets
        
    def refresh_equipment_widget(self, player):
        def open_equipment(typ, button):
            self.active_screen["state"] = typ
            
        def send_equip(item, button):
            if not item.is_equipped:
                player.equip(item)
            self.active_screen["state"] = "normal"
            
        def send_unequip(button):
            if self.active_screen["state"] in player.equipment:
                player.unequip(player.equipment[self.active_screen["state"]])
            
            self.active_screen["state"] = "normal"
                
        
        widgets = []
        
        if self.active_screen["state"] == "normal":
            t = urwid.Text("", align='center')
            widgets.append(t)
            
            for e in ["Weapon", "Armor", "Helm", "Belt", "Gloves", "Boots"]:
                b = urwid.Button("{}".format(e))
                b._label.align = 'center'
                w = urwid.AttrMap(b,None,"line")
                urwid.connect_signal(b, "click", open_equipment, user_args = [e])
                    
                if e in player.equipment:
                    i = player.equipment[e]
                    bonus = ",".join([" {}: {} ".format(bns, i.bonus[bns]) for bns in i.bonus if i.bonus[bns]!=0])
                    text = urwid.Text([(i.rarity, "{} ".format(i.name)), bonus])
                else:
                    text = urwid.Text("None")
                line = [(16, w), text]
                columns = SelectableColumns(line, dividechars=2)
                widgets.append(columns)    
                    
            bonus = player.bonus.copy()            
            for obj in player.equipment:
                for b in player.equipment[obj].bonus:
                    if b in bonus:
                        bonus[b] += player.equipment[obj].bonus[b]
                    
            t.set_text(" ".join(["{:3}: {:<2}".format(b, bonus[b]) for b in bonus]))
        else:
            t = urwid.Text("{}".format(self.active_screen["state"]), align='center')
            widgets.append(t)
            b = urwid.Button("None")
            b._label.align = 'center'
            w = urwid.AttrMap(b,None,"line")
            urwid.connect_signal(b, "click", send_unequip)
            text = urwid.Text("")
            line = [(16, w), text]
            columns = SelectableColumns(line, dividechars=2)
            widgets.append(columns)
            eqs = [i for i in player.inventory if i.type == self.active_screen["state"] and i.requisites(player)]
            for i in eqs:
                bonus = ",".join([" {}: {}".format(bns, i.bonus[bns]) for bns in i.bonus if i.bonus[bns]!=0]) + " " + ",".join([" {}: {} ".format(ab, i.abilities[ab].name) for ab in i.abilities] )
                b = urwid.Button(i.name)
                b._label.align = 'center'
                text = urwid.Text("{} {}".format(bonus, "(eq)"*int(i.is_equipped)))
                w = urwid.AttrMap(b,i.rarity,"line")
                urwid.connect_signal(b, "click", send_equip, user_args = [i])
                line = [(16, w), text]
                columns = SelectableColumns(line, dividechars=2)
                widgets.append(columns)
            
        self.active_screen["widget"].body[:] = widgets
        
  
                  
class SelectableListBox(urwid.ListBox):
    def __init__(self, body):
        super(SelectableListBox, self).__init__(body)

    def focus_next(self):
        try: 
            self.focus_position += 1 
        except:
            pass
    def focus_previous(self):
        try: 
            self.focus_position -= 1
        except:
            pass  
            
class InventorySelectableColumns(urwid.Columns):
    def __init__(self, widget_list, index, dividechars=0):
        super(InventorySelectableColumns, self).__init__(widget_list, dividechars)
        self.index = InventorySelectableColumns
    def focus_next(self):
        try: 
            self.focus_position += 1 
            self.index += 1
        except:
            pass
    def focus_previous(self):
        try: 
            self.focus_position -= 1
            self.index = 1
        except:
            pass   
            
class SelectableColumns(urwid.Columns):
    def __init__(self, widget_list, dividechars=0):
        super(SelectableColumns, self).__init__(widget_list, dividechars)
        
    def focus_next(self):
        try: 
            self.focus_position += 1 
        except:
            pass
    def focus_previous(self):
        try: 
            self.focus_position -= 1
        except:
            pass
        
def log(text):
    with open("log.tiac", "a") as f:
        f.write("{}: {}\n".format(time.time(), text))


        
