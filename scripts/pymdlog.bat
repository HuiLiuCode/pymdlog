@echo off
mshta vbscript:createobject("wscript.shell").run("pymdlogwin.bat",0)(window.close)&&exit
