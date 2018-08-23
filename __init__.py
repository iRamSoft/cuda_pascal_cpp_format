import os
import shutil
import subprocess
import tempfile
from cudatext import *

ini = os.path.join(app_path(APP_DIR_SETTINGS), 'pascal_cpp_formater.ini')
ini0 = os.path.join(os.path.dirname(__file__), 'settings.sample.ini')

if os.path.isfile(ini0) and not os.path.isfile(ini):
    shutil.copyfile(ini0, ini)

#-------options
opt_formater_dir = ini_read(ini, 'op', 'formater_directory', '')
#--------------   

def _getFormaterPath():
    return os.path.join(opt_formater_dir,'formatter.exe')    

def _getConfigFileName():
    return os.path.join(opt_formater_dir,'formatter.config')

def _format_source_code(source_text):
    try:
        s = source_text.replace('\r', '')
        
        fx = tempfile.NamedTemporaryFile(delete=False)
        file_name = fx.name
        fx.close()
        
        with open(file_name, 'w') as f:
            f.write(s)
    
        if ed.get_prop(PROP_LEXER_FILE, '').lower() == 'c++':
          rad_opt = '-cpp'
        else:
          rad_opt = '-delphi' 
    
        cmd = '"{}" {} {} "{}"'.format(_getFormaterPath(), rad_opt, '-config "{}"'.format(_getConfigFileName()) \
            if os.path.isfile(_getConfigFileName()) else '', file_name)
            
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        out, err = proc.communicate()
        proc.stdout.close()        
        
        if err:
            msg_status('Pascal/C++ Format: {}'.format(err))
        else:    
            msg_status('Pascal/C++ Format: {} {}'.format(ed.get_filename(), 'formated'))
        
        with open(file_name, 'r') as f:
            s = f.read().replace('\n', '\r\n')

        os.remove(file_name)
    
        return s
    except:
        raise    
    
def _checks():
    if not os.path.isfile(_getFormaterPath()):
        if msg_box('Path parameters for "formatter.exe" are not specified.\r\nOpen the settings file?', \
            MB_OKCANCEL+MB_ICONQUESTION) == ID_OK:
            file_open(ini)    
        return False
    else:
        return True   
    
    
class Command:
    def format_selected(self):
        if not _checks(): return
        try:
            carets = ed.get_carets()
            if len(carets)!=1: 
                msg_status('Pascal/C++ Format: multi-carets not supported')
                return
                
            x0, y0, x1, y1 = carets[0]
            if (y0, x0)>(y1, x1):
                x0, y0, x1, y1 = x1, y1, x0, y0
            
            s = _format_source_code(ed.get_text_substr(x0, y0, x1, y1))

            if not s:
                msg_status("Pascal/C++ Format: Cannot format text")
                return

            ed.set_caret(x0, y0)
            ed.delete(x0, y0, x1, y1)
            ed.insert(x0, y0, s)

        except:
            raise

    def format_full(self):
        if not _checks(): return
        try:
            s = ed.get_text_all()
            alllen = len(s)
            s = _format_source_code(s)
            
            if not s:
                msg_status("Pascal/C++ Format: Cannot format text")
                return
            
            ed.set_caret(0, 0)
            ed.set_text_all(s)           
        except:
            raise
            
    def config(self):
        file_open(ini)

    def open_formater_config(self):
        if not os.path.isfile(ini0):
            msg_box('File "formatter.config" not found in directory "{}"'.format(opt_formater_dir), MB_OK+MB_ICONERROR)
        else:
            file_open(_getConfigFileName())
        