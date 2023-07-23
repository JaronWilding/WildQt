# from WildQt.Windows import CreateUI


import win32api

def getFileDescription(windows_exe):
    try:
        language, codepage = win32api.GetFileVersionInfo(windows_exe, '\\VarFileInfo\\Translation')[0]
        stringFileInfo = u'\\StringFileInfo\\%04X%04X\\%s' % (language, codepage, "FileDescription")
        description = win32api.GetFileVersionInfo(windows_exe, stringFileInfo)
    except:
        description = "unknown"
        
    return description
    
    
print(getFileDescription(r"C:\Program Files\Internet Explorer\iexplore.exe"))