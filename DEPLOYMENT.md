
# Deployment der Todolist-App auf einem Raspberry Pi mit Docker

Dieses Dokument beschreibt Schritt für Schritt, wie die Todolist-Webanwendung auf einem Raspberry Pi bereitgestellt wird. Die Anwendung läuft in einem Docker-Container und wird über den von Flask bereitgestellten Webserver ausgeliefert. Der Raspberry Pi verwendet dabei eine statische IP-Adresse zur besseren Erreichbarkeit im Netzwerk.




## Ausgangssituation und erste Schritte

#### Benötigte Ressourcen

Um den Server einzurichten werden folgende Ressourcen benötigt:

- Raspberry Pi 3
- SD-Karte mit Raspberry Pi OS
- Root Rechte

#### Erste Schritte

Im verlaufe dieses Dokuments wird der Befehl **sudo** genutzt, dieser sorgt dafür, dass ein Befehl mit Root-Rechten ausgeführt wird.

Bevor mit der Konfiguration begonnen werden kann, müssen die aktuellsten Softwarepakete installiert werden. Dazu müssen folgende Befehle ausgeführt werden:

Paketlisten aktualisieren

```bash
sudo apt-get update
```

Die neuesten Versionen der Pakete installieren

```bash
sudo apt-get upgrade
```


## Netzwerkkonfiguration

Im folgenden Abschnitt wird die Netzwerkkonfiguration des Systems beschrieben. Dabei wird zunächst der SSH-Zugriff aktiviert und eine statishe IP vergeben

#### SSH einrichten

SSH starten

```bash
sudo systemctl start ssh
```

SSH bei einem Neustart automatisch starten

```bash
sudo systemctl enable ssh
```

#### Statische IP vergeben

DHCP konfiguration öffnen

```bash
sudo nano /etc/dhcpcd.conf
```

*nano* – öffnet eine Datei in einem Texteditor

Folgenden Abschnitt in der config ändern

```bash
interface INTERFACE
static ip_address=STATISCHE_IP/24
static routers=GATEWAY
static domain_name_servers=GATEWAY
```

*static ip_address* – Die Statische IP-Adresse, über die der Server erreicht werden soll

*static routers* – Das Gateway Ihres Netzwerks

*static domain_name_servers* - Die IP-Adresse Ihres DNS-Servers

Die großgeschriebenen Begriffe mit den benötigten Adressen ersetzen.

Anschließend die Datei speichern *(STRG + O)* und schließen *(STRG + X)*








## Lokale Benutzer anlegen

Dieser Abschnitt erläutert, wie lokale Benutzer mit unterschiedlichen Rechten angelegt werden

#### Benutzer anlegen

Neuen Benutzer anlegen

```bash
sudo adduser USERNAME
```

Sie werden aufgefordert, eine Reihe von Fragen zu beantworten:

- Vergeben und bestätigen Sie ein Passwort für den neuen Benutzer
- Geben Sie zusätzliche Informationen über den neuen Benutzer ein *(optional)*
- Abschließend werden Sie aufgefordert, die Richtigkeit der von Ihnen eingegebenen Informationen zu bestätigen. Drücken Sie Y, um fortzufahren

#### Benutzer mit Rootrechten anlegen

Um einem Benutzer Rootrechte zu verleihen, muss dieser in die Sudogruppe hinzugefügt werden

Benutzer in die Sudogruppe hinzufügen

```bash
sudo usermod -aG sudo USERNAME
```

**-aG** – Fügt den Benutzer zur angegebenen Gruppe hinzu
## Installation und Einrichtung eines Docker Containers

Damit die Webanwendung vom Hostsystem isoliert bereitgestellt werden kann, muss ein Container erstellt werden.

#### Docker installieren und einrichten

Docker installieren

```bash
sudo apt install docker.io
```

Docker-Dienst starten

```bash
sudo systemctl start docker.service
```

Docker bei einem Neustart automatisch starten

```bash
sudo systemctl enable docker.service
```

Docker Installation testen

```bash
sudo docker run hello-world
```

Mit diesem Befehl wird ein einfaches "Hello-World"-Programm aus Docker-Hub installiert und gestartet um die Funktionalität zu testen.

#### Docker Image erstellen

Damit die Docker-Anwendung korrekt läuft, muss ein Docker Image erstellt werden, welches durch eine Dockerfile realisiert wird. Diese muss sich im selben Verzeichnis wie die Webanwendung befinden. Dafür muss das Projektverzeichnis auf den Raspberry Pi kopiert werden und anschließend eine Dockerfile erstellt werden.



Dockerfile erstellen

```bash
sudo nano Dockerfile
```

Die Dockerfile sollte folgende Konfiguration beinhalten:

```bash
FROM python:3.8-alpine

RUN pip install flask

WORKDIR /app

COPY . /app

CMD ["python", "server.py" ]
```

*FROM python:3.8-alpine* – Legt das Basis Image fest

*RUN pip install flask* – Installiert das Flask-Webframework

*WORKDIR /app* – Verlegt das Arbeitsverzeichnis innerhalb des Containers auf /app

*COPY . /app* – Kopiert alle Dateien aus dem aktuellen Verzeichnis in das Verzeichnis /app im Container

*CMD ["python", "server.py"]* – Führt beim Start des Containers die Webanwendung aus

Anschließend die Datei speichern (STRG + O) und schließen (STRG + X)

Docker Image bauen

```bash
sudo docker image build -t webapp .
```

**-t** –  Übergibt dem Image einen Namen

#### Docker Container ausführen

Container mit dem erstellten Image starten

```bash
sudo docker run -p 5000:5000 -d --name todolistmanager webapp
```

**-p 5000:5000** –  Mapped den Hostport 5000 mit dem Containerport 5000

**-d** – Startet den Container im detached-mode damit man sich nicht in der Konsole des Python-Skripts befindet

**--name todolistmanager** – Übergibt dem Container den Namen "todolistmanager"

Die Webseite kann nun unter der zuvor statisch angelegegten IP und Port 5000 im Browser erreicht werden

#### Nützliche Docker Befehle

Images anzeigen

```bash
sudo docker images
```

Laufende Container anzeigen

```bash
sudo docker ps
```

Container starten und stoppen

```bash
sudo docker start todolistmanager
sudo docker stop todolistmanager
```
