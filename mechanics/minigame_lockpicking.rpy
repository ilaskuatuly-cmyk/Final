init python:
    import pygame
    import renpy.store as store
    
    # Register channels
    renpy.music.register_channel("Lock_Move", mixer= "sfx", loop=True)
    renpy.music.register_channel("Lock_Click", mixer= "sfx", loop=False, tight=True)

    # Images definition
    lock_img_paths = ["images/lock_plate.png", "images/lock_cylinder.png",
                      "images/lock_tension.png", "images/lock_pick.png"]

    class Lock(renpy.Displayable):
        def __init__(self, difficulty, resize=1920, **kwargs):
            super(Lock, self).__init__(**kwargs)
            
            self.width = resize
            # Scaling images
            self.lock_plate_image = im.Scale(lock_img_paths[0], resize, resize)
            self.lock_cylinder_image = im.Scale(lock_img_paths[1], resize, resize)
            self.lock_tension_image = im.Scale(lock_img_paths[2], resize, resize)
            self.lock_pick_image = im.Scale(lock_img_paths[3], resize, resize)
            
            self.offset = (resize*2**0.5-resize)/2
            
            # Game Logic Variables
            self.cylinder_min = 0
            self.cylinder_max = 90
            self.cylinder_pos = 0 
            self.cylinder_try_rotate = False 
            self.cylinder_can_rotate = False 
            self.cylinder_released = False 
            
            self.pick_pos = 90
            self.pick_can_rotate = True
            self.sweet_spot = renpy.random.randint(0,180) 
            self.difficulty = difficulty 
            self.breakage = (difficulty/7 + 0.75)
            self.timers = 0
            self.set_timers = False
            self.pick_broke = False

        def event(self, ev, x, y, st):
            LEFT = 1
            RIGHT = 3
            
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == LEFT:
                if store.current_lockpicks > 0:
                    self.cylinder_try_rotate = True
                    self.cylinder_released = False
                    
            elif ev.type == pygame.MOUSEBUTTONUP and ev.button == LEFT:
                renpy.sound.stop(channel="Lock_Move")
                self.cylinder_try_rotate = False
                self.cylinder_released = True
                self.pick_can_rotate = True
                self.pick_broke = False
                
            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == RIGHT:
                renpy.end_interaction(False)

        def render(self, width, height, st, at):
            diff = max(1, min(29, self.difficulty))
            if self.pick_can_rotate:
                mx, my = renpy.get_mouse_pos()
                self.pick_pos = mx/5.3333333333 - 90 
                self.pick_pos = max(0, min(180, self.pick_pos))
                delta = abs(self.pick_pos - self.sweet_spot)
                self.cylinder_can_rotate = True
                if delta < diff:
                    self.cylinder_max = 90 
                else:
                    self.cylinder_max = max(0, 90 - delta*(30/diff))

            if self.pick_broke:
                pick = Transform(child=None)
            else:
                pick = Transform(child=self.lock_pick_image, rotate=self.pick_pos, subpixel=True)

            if self.cylinder_try_rotate and store.current_lockpicks > 0:
                self.cylinder_pos += (2*st)/(at+1)
                if self.cylinder_pos > self.cylinder_max:
                    self.cylinder_pos = self.cylinder_max
                    if self.cylinder_pos >= 90:
                        renpy.sound.stop(channel="Lock_Move")
                        renpy.sound.play("audio/lock_unlock.mp3", channel="Lock_Click")
                        pygame.time.wait(150)
                        renpy.end_interaction(True)
                    else:
                        if not renpy.sound.is_playing(channel="Lock_Move"):
                            renpy.sound.play("audio/lock_moving.mp3", channel="Lock_Move")
                        if not self.set_timers:
                            self.timers = at
                            self.set_timers = True
                        if at > self.timers + self.breakage:
                            renpy.sound.stop(channel="Lock_Move")
                            renpy.sound.play("audio/lock_pick_break.mp3", channel="Lock_Click")
                            renpy.notify("Отмычка сломалась!")
                            self.pick_can_rotate = False
                            self.pick_broke = True
                            self.cylinder_try_rotate = False
                            store.current_lockpicks -= 1
                            self.set_timers = False
                            if store.current_lockpicks <= 0:
                                renpy.end_interaction(False)
                            pygame.time.wait(200)
            else:
                if self.cylinder_released:
                    if self.cylinder_pos > 15:
                         renpy.sound.play("audio/lock_moving_back.mp3", channel="Lock_Click")
                    self.pick_can_rotate = True
                    self.cylinder_pos -= (5*st)/(at+1)
                    if self.cylinder_pos < self.cylinder_min:
                        self.cylinder_pos = self.cylinder_min
                        self.cylinder_released = False
                        renpy.sound.stop(channel="Lock_Click")

            c_angle = self.cylinder_pos
            t_angle = self.cylinder_pos
            if self.cylinder_try_rotate and self.cylinder_pos >= self.cylinder_max and self.cylinder_pos < 90:
                 c_angle += renpy.random.randint(-2,2)
                 t_angle += renpy.random.randint(-4,4)

            cylinder = Transform(child=self.lock_cylinder_image, rotate=c_angle, subpixel=True)
            tension = Transform(child=self.lock_tension_image, rotate=t_angle, subpixel=True)

            lock_plate_render = renpy.render(self.lock_plate_image, width, height, st, at)
            lock_cylinder_render = renpy.render(cylinder, width, height, st, at)
            lock_tension_render = renpy.render(tension, width, height, st, at)
            lock_pick_render = renpy.render(pick, width, height, st, at)

            render = renpy.Render(self.width, self.width)
            render.blit(lock_plate_render, (0, 0))
            render.blit(lock_cylinder_render, (-self.offset, -self.offset))
            render.blit(lock_tension_render, (-self.offset, -self.offset))
            render.blit(lock_pick_render, (-self.offset, -self.offset))
            
            renpy.redraw(self, 0)
            return render

image lock_dark = Solid("#000c")

screen lockpicking_game(difficulty=20):
    default lock_obj = Lock(difficulty, 1000)
    
    add "lock_dark"
    add lock_obj xalign 0.5 yalign 0.5

    vbox:
        xalign 0.05
        yalign 0.05
        text "Отмычки: [current_lockpicks]" size 40 color "#fff"
        text "Цель: Вскройте замок!" size 30 color "#ccc"

    # Button to give up
    textbutton "Сдаться":
        xalign 0.9
        yalign 0.95
        action Return(False)

    textbutton "Пропустить экзамен":
        xalign 0.98
        yalign 0.02
        action Return("skip")
        text_size 16
        text_color "#bdc3c7"
        text_hover_color "#fff"
