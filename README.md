# ESY

## Installation

Zuerst wird das Repository geklont:
``` bash
git clone https://github.com/slanda156/rpi-gpio-lesson
cd rpi-gpio-lesson
```

Die einstiegs Datei in das Programm muss ausfürbar gemacht werde.

``` bash
sudo chmod ug+x main.py
```

Als Nächstes wird ein virtuelles Environment erzeugt und aktiviert:
``` bash
python -m venv .venv
sourve ./venv/bin/activate
```

Nun installieren wir die benötigten Module:
``` bash
pip install pip-tools
pip-compile
pip-sync
```

Jetzt sollten das Programm und alle Abhängigkeiten installiert sein.

## Nutzung des Programms

Das Programm kann nun gestartet werden, solange das Virtuale Environment aktiv ist.

``` bash
./main.py
```

## Aufgaben

1. Gehe auf den Tab mit dem Tilt-Sensor. Kippe den Sensor und beobachte die Anzeige im Programm. Notiere deine Beobachtung.

2. Gehe auf den Tab mit der RGB-LED. Nutze die Schalter im Programm, um die LED zu steuern. Beobachte die entstehenden Farben.
Notiere, wie viele Farben mit drei Schaltern möglich sind. Sind alle Farben gleich hell?

3. Gehe auf den Tab mit dem Heartbeat-Sensor. Halte einen Finger vor den Sensor. Zum Messen muss der Schalter im Programm eingeschaltet werden.
Beobachte den Graphen. Was fällt dir auf?
Versucht euren Herzschlag pro Minute zu messen.

4. Gehe auf den Tab mit dem Tilt-Sensor und der LED.
Kippt den Sensor. Notiert, wie der Sensor die LED beeinflusst.

5. Gehe auf den Tab mit dem Heartbeat-Sensor und der LED.
Beobachtet und notiert das Verhalten der LED.

### Meta

Christoph Heil – <christoph.heil156@gmail.com>

Veröffentlicht unter der MIT-Lizenz. Siehe [``License``](LICENSE) für weitere Informationen.

[https://github.com/slanda156/rpi-gpio-lesson](https://github.com/slanda156/rpi-gpio-lesson)
