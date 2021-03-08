# library-dashboard
Dieses Repository enthält den Programmcode für das Proof-of-Concept der Masterarbeit "Konzeption und Entwicklung eines datengetriebenen Unterstützungssystems für Etatplanung und Mittelallokation einer hybriden Spezialbibliothek" an der TH-Wildau im Studiengang Bibliotheksinformatik (Wildau Institute of Technology, WIT). Im Rahmen der Masterarbeit wurde ein Dashboard entwickelt, das Bibliotheksdaten aus den Bereichen Umsatz, Budget, Bestandsentwicklung, Ausleihe und Lesesaalnutzung der Bibliothek des
Max-Planck-Instituts für empirische Ästhetik anzeigt. Desweiteren enthält das Repository Skripte für die Steuerung des Imports von Daten aus heterogenen Datenquellen, die der Bibliothek bereitgestellt werden. Im vorliegenden Repository werden lediglich randomisierte Testdaten zur Verfügung gestellt, momentan aus den Bereichen Umsatz und Budget. Aufgrund dieser Datenlage läuft das Dashboard eingeschränkt. Der Programmcode ist entsprechend für die Anzeige des Tabs "Umsatz und Budget" eingestellt. Die Ausführung der Skripte (Datenimport) ist aufgrund der eingeschränkten Datenlage noch nicht möglich. 
Der Programmcode ist vollständig, lediglich die Originaldaten werden nicht zur Verfügung gestellt. Sukzessive werden Testdaten bereitgestellt.

# Installation

Die Datei requirements.txt listet alle Python-Bibliotheken auf, die für die Ausführung des Projekts benötigt werden. 
Sie werden installiert durch:

```
> pip3 install -r requirements.txt
```

Im Moment muss noch der PYTHONPATH exportiert werden.
```
> export PYTHONPATH="${PYTHONPATH}:/path/to/the/project_folder"
```

um alle Module im Projektverzeichnis zu finden.

# Start

Um die Anwendung auszuführen, gehen Sie bitte in den Ordner dashboard im Projektverzeichnis
und geben auf der Kommandozeile folgendes ein:

```
> python index.py
```

```
Dash is running on http://0.0.0.0:8050/

 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
```

Diese Anweisung startet den Webserver und die Adresse kann durch einen gängigen Browser aufgerufen werden. 


# Bemerkungen
Testdaten werden in Zukunft sukzessive hinzugefügt.


# Roadmap
[ ] Testdaten\
[ ] Code Refactoring\
[ ] Python Package Building\
[ ] Tests mit pytest oder unitests\
[ ] Open Source Lizenz


# Autor

Peter Breternitz