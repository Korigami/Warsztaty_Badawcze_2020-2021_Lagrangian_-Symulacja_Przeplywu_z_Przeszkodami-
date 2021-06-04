# Warsztaty_Badawcze_2020-2021_Lagrangian

## Przygotowanie środowiska
Przed uruchomieniem aplikacji należy przygotować środowisko. Ze względu na używane w kodzie paczki należy zainstalować moduły znajdujące się w pliku **python-requirements.txt**. W tym celu można wykorzystać 
 -  skrypt **makevenv.sh** (w przypadku Linuxa)
     
    ```console 
    sudo bash makevenv
    source /venv/bin/activate
    ```
  
 -  następujące polecenia (w przypadku Windowsa)
    
    ```console
    python3 -m venv venv
    venv/Scripts/activate.bat
    python3 -m pip install -r python-requirements.txt
    ```
Aby móc stworzyć wirtualne środowisko należy zaistalować odpowiednie pakiety. Można wykorzystać:
 -  skrypt **install_venv_ubuntu.sh** (w przypadku Linuxa)
 
 -  skrypt **install_venv_windows.bat** (w przypadku Windowsa)

Aby deaktywować wirtualne środowisko po zakończeniu pracy wystarczy wpisać 
```console
deactivate
```
## Uruchomienie
Aby uruchomić aplikację należy
 - zbudować pakiet `Octree`. Aby to zrobić należy wejść do katalogu `Octree` i wykonać komendę 
    ```console
    python3 setup.py build_ext --inplace
    ```
 - uruchomić skrypt `run.py` za pomocą komendy
    ```console 
    python3 run.py
    ```
## Raport
Raport z opisem działania poszczególnych części projektu dostępny jest w pliku ''raport.pdf''. Można również przejść do niego bezpośrednio przy pomocy <object data="https://github.com/Korigami/Warsztaty_Badawcze_2020-2021_Lagrangian_-Symulacja_Przeplywu_z_Przeszkodami-/blob/main/Raport.pdf" type="application/pdf" width="700px" height="700px">
    <embed src="https://github.com/Korigami/Warsztaty_Badawcze_2020-2021_Lagrangian_-Symulacja_Przeplywu_z_Przeszkodami-/blob/main/Raport.pdf">
        <p>This browser does not support PDFs. Please download the PDF to view it: <a href="https://github.com/Korigami/Warsztaty_Badawcze_2020-2021_Lagrangian_-Symulacja_Przeplywu_z_Przeszkodami-/blob/main/Raport.pdf">linku</a>.</p>
    </embed>
</object>

