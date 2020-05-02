#include <gtk/gtk.h>
#include <gdk/gdk.h>
#include <glib-2.0/glib.h>

void onDestroy( GtkWidget *widget, gpointer data){
    
    gtk_main_quit();

}

int main( int argc, char *argv[] ){
    GtkBuilder *builder;
    GObject *window, *spinner;
    
    
    gtk_init( &argc, &argv);

    builder = gtk_builder_new();

    gtk_builder_new_from_file("ui/window_wait_payment.glade");
    window = gtk_builder_get_object(builder, "window_wait_payment");
    spinner = gtk_builder_get_object(builder, "spinner");
    
    g_signal_connect (window, "destroy", G_CALLBACK (gtk_main_quit), NULL);

    gtk_main();
    return 0;

}