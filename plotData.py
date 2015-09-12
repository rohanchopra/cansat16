#!/usr/bin/python3


from gi.repository import Gtk
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas



line = ''
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
xar = []
yar = []
canvas = FigureCanvas(fig)


class Signals:
    def on_window1_destroy(self, widget):
        sys.exit(0)
    def on_quit_clicked(self,widget):
        sys.exit(0)
        
    def on_button1_clicked(self, button):
        canvas.print_figure('ultrasonic_graph')
        
    def on_togglebutton1_toggled(self, button):
        if button.get_active():
            state = ['1', 'on']
            button.set_label(state[1].upper())
            self.send_command(state[0])
        else:
            state = ['0', 'off']
            button.set_label(state[1].upper())
            self.send_command(state[0])
            
    def send_command(self, val):
      global ser
      ser.write(val.encode())
      
      
builder = Gtk.Builder()
builder.add_objects_from_file('toggleLed.glade', ('applicationwindow1', '') )
builder.connect_signals(Signals())

myfirstwindow = builder.get_object('applicationwindow1')
sw = builder.get_object('scrolledwindow1')
        
        
def animate(i):
    global line
    global ser
    global xar,yar
    global canvas
    
    
    
    
    
    print("xar = ")
    print(xar)
    print("yar = ")
    print(yar)
    
    ax1.clear()
    ax1.plot(xar,yar)
    ax1.set_title('Ultrasonic Sensor Readings')
    
    
    
    canvas = FigureCanvas(fig)
    if (sw.get_child()!=None):
      sw.remove(sw.get_child())
    sw.add(canvas)
    myfirstwindow.show_all()
    
    print ("Time taken: ")
    print(time.time() - start)
    


# main() function
def main():
  ani = animation.FuncAnimation(fig , animate , interval=1000)
  Gtk.main()
  plt.ylim((0,100))
  plt.xlim((0,240))
  
# call main
if __name__ == '__main__':
  main()

