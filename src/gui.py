import gtk

class OurGui(gtk.Window):

  def __init__(self):
    gtk.Window.__init__(self)
    
    self.set_title('Our Gui')
    self.set_size_request(300, 200)
    self.connect('destroy', gtk.main_quit)

    self.vbox = gtk.VBox()

    self.go_button = gtk.Button('_Go')
    self.go_button.connect('clicked', self.print_out)
    
    self.quit_button = gtk.Button('_Quit')
    self.quit_button.connect('clicked', gtk.main_quit)
    
    self.drawstuff_button = gtk.Button('Draw Stuff')
    self.drawstuff_button.connect('clicked', self.draw_stuff)

    self.vbox.pack_start(gtk.Label('click here'), False)
    self.vbox.pack_start(self.go_button, False)
    self.vbox.pack_start(self.drawstuff_button, True)
    self.vbox.pack_end(self.quit_button, False)

    self.add(self.vbox)

  def print_out(self, *_args):
    print 'hi'
    
  def draw_stuff(self, *_args):
    dlg = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
    dlg.set_markup("Not implemented yet.")
    _response = dlg.run()
    dlg.destroy()
    
  def run(self):
    self.show_all()
    gtk.main()

app = OurGui()
app.run()