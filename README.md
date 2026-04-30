# prosjekt_forum
## Logg – Feilsøking MariaDB og Flask

I dag jobbet jeg med å koble Flask-applikasjonen min mot MariaDB-databasen på serveren.

Først fikk jeg feilmeldingen **Access denied for user** når Python skulle koble til databasen. Jeg startet derfor feilsøking av brukertilgang, nettverk og databaseinnstillinger.

### Arbeid som ble gjort:

* Logget inn på Linux-serveren via terminal.
* Navigerte til MySQL/MariaDB-konfigurasjonsfiler i `/etc/mysql/`.
* Sjekket filer som:

  * `my.cnf`
  * `mariadb.cnf`
  * `50-server.cnf`
* Kontrollerte at `bind-address` tillater eksterne tilkoblinger.
* Sjekket brannmur med `ufw status`.
* Bekreftet at port **3306** var åpen for MariaDB.
* Logget inn i MariaDB som administrator.
* Sjekket brukerrettigheter for brukeren `abdi`.

### Løsning:

Jeg oppdaget at brukeren ikke hadde riktige rettigheter for ekstern tilgang. Derfor kjørte jeg:

```sql
ALTER USER 'abdi'@'%' IDENTIFIED BY 'abdisemed08';
GRANT ALL PRIVILEGES ON skjema_db.* TO 'abdi'@'%';
FLUSH PRIVILEGES;
```

### Resultat:

Etter dette fungerte tilkoblingen mellom Flask og MariaDB. Python-programmet kunne koble til databasen og lagre data fra HTML-skjemaet.

### Hva jeg lærte:

* Hvordan MariaDB-brukere styres med `user@host`
* Hvordan gi rettigheter med `GRANT`
* Hvordan åpne porter i Linux-brannmur
* Hvordan Flask kobles mot ekstern database
* Hvordan feilsøke databaseforbindelser systematisk
