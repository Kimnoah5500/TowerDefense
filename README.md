# Dokumentation

## Projekt-Beschreibung
Entwickelt wird ein Tower Defense spiel mit Python, bei diesem Spiel wandern Gegner entlang eines vorgegebenen Wegs, der Spieler hat die Möglichkeit sogenannte "Tower" zu bauen die auf die Gegner schießen.
Dabei gibt es verschiedene Gegner sowie auch verschiedene Tower mit unterschiedlichen Lebenspunkten bzw Stärken.
Die Tower kann der Spieler frei auf dem Spielfeld platzieren nachdem er diese gekauft hat und diese nach dem Platzieren mit Upgrades ausstatten.
Durch das Abschießen von Gegnern erhält der Spieler Münzen von denen er dann wie erwähnt Türme und Upgrades kaufen kann. 
Sollte ein Gegner ohne abgeschossen zu werden bis ins Ziel kommen verliert der Spieler Lebenspunkte. 
Ziel für den Spieler ist es eine bestimmte Anzahl von Wellen zu überstehen ohne dabei alle Lebenspunkte zu verlieren.
Es wird vorgefertigte Level mit unterschiedlichen Karten und Wegen für die Gegner geben, ein Level Editor zum erstellen eigener Karten ist nicht geplant.
Auch eine hübsche Grafik ist mangels Grafiker Kenntnisse bei uns nicht zu erwarten.

## Zielplattform
Auf Windows 10 und MacOS entwickelt. Generell ausführbar auf allen Systemen die Python-Programme laufen lassen können (keine Garantie abseits Windows und MacOS).

## Liste der einzelnen Module
* board
  * Beinhaltet und verwaltet das Spielfeld 
* button
  * Hilfsmodul zur Erstellung von pygame-Buttons
* damage_types
  * Beinhaltet ein Enum zur Verwaltung der verschiedenen Schadenstypen
* enemy
  * Beinhaltet Klassen zur Erstellung und Verwaltung von Gegnern
* field
  * Beinhaltet Klassen für die Verschiedenen Felder
* main
  * Beinhaltet die Hauptklasse, die das Spiel initalisiert und steuert
* player
  * Beinhaltet die Daten des Spielers und möglichkeiten diese zu verwalten
* projectile
  * Beinhaltet die Verschiedenen Geschoss-Klassen und eine Klasse zur Verwaltung selbiger
* shop
  * Beinhaltet den Shop und funktionen um diesen zu erstellen und zu verwalten
* text_box
  * Hilfsmodul zur Erstellung und Darstellung von Textboxen mittels pygame
* tower
  * Beinhaltet die Verschiedenen Turm-Klassen und eine Klasse für die Verwaltung
  
*Für eine genauere Beschreibung der Klassen und deren Funktionen verweisen wir auf die ausfürhliche Dokumentation des gesamten Codes.*

## Abhängigkeiten
Zur Verwendung des Projekts wird die aktuelste dev-version von pygame benötigt, diese kann mithilfe des Befehls `pip install --upgrade pygame --pre` installiert werden.

## Erziehltes Resultat
Bis auf eine Anforderung wurden alle Spezifikationen erfüllt. 

Was aufgrund der Zeit leider nicht mehr möglich war zu implementieren, ist eine Upgradefunktion für die einzelnen Türme.
Einmal platzierte Türme lassen sich also nur noch wieder verkaufen, nicht mehr verbessern.

*Im Spiel selbst steht eine Hilfe-Seite zur verfügung die nochmals das Spiel mitsamt den Regeln und Funktionen erklärt.*
*Btw. das Scrollrad kann man hier zum durchblättern benutzen ;)*

Auch bekannt ist, das an manchen wenigen stellen nicht nach dem "Pythonic way of Coding" programmiert wurde, zur Behebung davon würden nochmals ca. 1-2 Tage an Programmierarbeit anfallen.

Auch Sounds bzw Musik wurden nicht in das Projekt mit eingebunden, hier würden nochmals ca. 2-3 Tage an Programmierarbeit anfallen.
