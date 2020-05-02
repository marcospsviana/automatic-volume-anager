using Gtk;

int main(string[] args) {
    Gtk.init(ref args);
    Gtk.Box box = new Gtk.Box (Gtk.Orientation.VERTICAL, 1);
    var window = new Gtk.Window();
    var labelWait = new Gtk.Label(" Aguarde um momento ...\n Wait a moment ....");
    var spinner = new Gtk.Spinner();
    window.destroy.connect(Gtk.main_quit);
    window.set_position(CENTER);
    window.set_default_size(500, 300);
    window.border_width = 0;
   

 

    spinner.active =true;
    spinner.show();
    spinner.start();
    box.pack_start(labelWait, true, false, 0);
    box.pack_start(spinner, true, false, 0);
        

    
    
    window.set_title(" window com vala ");
    window.add(box);
    window.show_all();  

    Gtk.main();

    return 0;
}
