pyinstaller --hidden-import=pyi_splash --distpath "./" -n "Server-SriPandita" --noconfirm --console --onefile --splash ".icon/SriPandita-FTP-Server.png" --icon ".icon/SriPandita-FTP.ico" --clean  "Server_SriPandita.py"

pyinstaller --hidden-import=pyi_splash --distpath "./" -n "Client-SriPandita" --noconfirm --onefile --windowed --splash ".icon/SriPandita-FTP-Home.png" --icon ".icon/SriPandita-FTP.ico" --add-data "D:/Program Files/Python311/Lib/site-packages/customtkinter;customtkinter/" --clean "Client_SriPandita.py"

rmdir /S /Q build
del /Q /F "Client SriPandita.spec"
del /Q /F "Server SriPandita.spec"
del /Q /F "Client-SriPandita.spec"
del /Q /F "Server-SriPandita.spec"

::pyinstaller --onefile --hidden-import=pyi_splash --distpath "./test/" -n "Server-SriPandita" --noconfirm --console --splash ".icon/SriPandita-FTP-Server.png" --icon ".icon/SriPandita-FTP.ico" --add-data "D:/GitHub/TuBes_SisParTer_SriPandita/.icon/*;.icon/" --clean  "Server_SriPandita.py"

::pyinstaller --onefile --hidden-import=pyi_splash --distpath "./test" -n "Client-SriPandita" --noconfirm --windowed --splash ".icon/SriPandita-FTP-Home.png" --icon ".icon/SriPandita-FTP.ico" --add-data "D:/GitHub/TuBes_SisParTer_SriPandita/.icon/*;.icon/" --add-data "D:/Program Files/Python311/Lib/site-packages/customtkinter;customtkinter/" --clean "Client_SriPandita.py"
