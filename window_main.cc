#include <gtkmm.h>

int main(int argc, char *argv[])
{

  //auto app =
    //Gtk::Application::create(argc, argv,
     // "org.gtkmm.examples.base");
    Glib::RefPtr<Gtk::Builder> builder = Gtk::Builder::create_from_file("ui/coolbag_safe.glade");

   window = builder.get_object("mainwindow");

  //Gtk::Box box;
  //Gtk::Builder builder;

  //window.set_default_size(1024, 550);
  

  //return app->run(window);
  window.show();

  //Gtk.main();

}