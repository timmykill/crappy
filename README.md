# helper per esami in cui ci sono le prove d'esame disponibili ma non le soluzioni

## HOWTO:

* crea un gruppo telegram per l'esame, e un bot (utilizzando botfather è un'attimo)

* costruisci il file config.py con le seguenti:
	```
	token
	admin
	port
	nomeEsame
	```

* crea, dentro `res`, una cartella con nome della prova, e all'interno metti un file prova.pdf contenente il testo della prova (prova, prova, prova, prova, ...)


* entra nel gruppo, utilizza in comando `/set`

* enjoy
