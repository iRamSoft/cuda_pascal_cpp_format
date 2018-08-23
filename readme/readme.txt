Plugin for CudaText.

It allows to format source code for lexers Pascal and C++, using "formatter.exe" from Embarcadero RAD Studio, only for Windows
http://docwiki.embarcadero.com/RADStudio/Tokyo/en/Formatter.EXE,_the_Command_Line_Formatter

 
If selection is made (only normal selection supported) use "Plugins\Pascal/C++ Format\Formatting the selection", otherwise "Plugins\Pascal/C++ Format\Formatting file".

To run the plugin, you must specify the path to the directory where the formatter.exe is located. To do this, specify the required path in the plugin's "Options\Settings - plugins\Pascal/C++ Format\Config" settings.

Optionally, you can use the "formatter.config" file for the formatting settings. The file should be located in the directory of the directory as "formatter.exe".

Authors:
  Khomutov Roman
License: MIT
