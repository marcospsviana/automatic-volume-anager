using Gtk;


class MainWindow{

static int main(string[] args){
    Gtk.init(ref args);
    //Gtk Builder for import glade file
    var builder = new Gtk.Builder();
        
    //Widget Gtk Window
    var window = new builder.from_file("ui/coolbag_safe.glade");
    builder.connect_signals(null);
    
    //============= Child Widgets =======================//
    //Show date and hour
    var label_horario = builder.get_object("label_horario");
    var label_data = builder.get_object("label_data");
    var dateTime = new DateTime.now();
    print(dateTime.to_string());
    
    //Buttons Select Languages
    var btn_flag_br = builder.get_object("btn_flag_br");
    var btn_flag_usa = builder.get_object("btn_flag_usa");
    var btn_principal = builder.get_object("btn_principal");
    
  

    
    //connect signals  
    btn_flag_br.connect("button-press-event", onChangeLanguageBr);
    
    
    btn_flag_usa.connect("button-press-event", onChangeLanguageUsa);
    
    
    window.connect("destroy",Gtk.main_quit);
    
    


    Gtk.main();

    return 0; 
}

static void onChangeLanguageUsa(object obj, EventArgs args){
    print("clicou USA\n");
}
static void onChangeLanguageBr(object obj, EventArgs args){
    print("clicou BR\n");
}
}


