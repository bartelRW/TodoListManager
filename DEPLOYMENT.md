
# Deployment der Todolist-App auf einem Raspberry Pi mit Docker

Dieses Dokument beschreibt Schritt für Schritt, wie die Todolist-Webanwendung auf einem Raspberry Pi bereitgestellt wird. Die Anwendung läuft in einem Docker-Container und wird über einen Apache-Webserver ausgeliefert. Der Raspberry Pi verwendet dabei eine statische IP-Adresse zur besseren Erreichbarkeit im Netzwerk.




## Ausgangssituation

Um den Server einzurichten werden folgende Ressourcen benötigt:

- Raspberry Pi 3
- SD-Karte mit Raspberry Pi OS
- Root Rechte
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

Folgenden Abschnitt in der config ändern

```bash
interface INTERFACE
static ip_address=STATISCHE_IP/24
static routers=GATEWAY
static domain_name_servers=GATEWAY
```

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

Damit die Docker-Anwendung korrekt läuft, muss ein Docker Image erstellt werden, welches durch eine Dockerfile realisiert wird. Diese befindet sich im selben Verzeichnis wie die Webanwendung

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

ENTRYPOINT [ "python" ]
CMD ["server.py" ]
```

*FROM python:3.8-alpine* – Legt das Basis Image fest

*RUN pip install flask* – Installiert das Flask-Webframework

*WORKDIR /app* – Verlegt das Arbeitsverzeichnis innerhalb des Containers auf /app

*COPY . /app* – Kopiert alle Dateien aus dem aktuellen Verzeichnis in das Verzeichnis /app im Container

*CMD ["python", "server.py"]* – Führt beim Start des Containers die Webanwendung aus

Docker Image bauen

```bash
sudo docker image build -t webapp .
```

#### Docker Container ausführen

Container mit dem erstellten Image starten

```bash
sudo docker run -p 5000:5000 -d --name todolistmanager webapp
```

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