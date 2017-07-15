import gtk
class WaitWindow(gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self)
        wait_pixbuf = gtk.gdk.PixbufAnimation("wait.gif")
        pix = gtk.Image()
        pix.set_from_animation(wait_pixbuf)
        frame = gtk.Frame()
        frame.add(pix)
        self.add(frame)
        self.show_all()
        gtk.main()

if __name__ == "__main__": 
WaitWindow()