# Deze regel code importeert de time library. We hebben de sleep() functie van deze library nodig.
# Een library is kort gezegd een verzameling code die iemand anders geschreven heeft, die we in ons programma kunnen gebruiken door hem te importeren.
# Hierdoor hoeven we niet elke keer opnieuw het wiel uit te vinden als we een programma schrijven.
import time

# Hier importeren we de library die de robotarm bestuurt.
import robotArm

# Hier maken we onze "instance" van de Arm "class" uit de robotArm library. Je kan een class zien als een legoset, waar alle onderdelen in zitten en de instructies om hem te bouwen.
# Onze instance of onze doos van die set. We kunnen hem opbouwen en vertellen wat ie moet doen.
# We kunnen onze instance elke naam geven die we willen, voor dit voorbeeld heb ik gekozen voor de naam "arm".
# Als je wil kan je de naam veranderen, maar zorg er dan wel voor dat je hem overal verandert, anders raakt het programma in de war.
arm = robotArm.Arm()

# Deze regel code stuurt een instructie naar de arm om een onderdeel te bewegen.
# Zoals je kan zien bestaat de instructie uit verschillende onderdelen.
# Het eerste deel van de instructie roept onze instance van de robotarm aan, die we hiervoor gemaakt hebben.
# In het tweede deel kiezen we het onderdeel van de arm dat we willen bewegen, in dit geval de schouder.
# Het derde deel vertelt de robotarm welke kant de schouder op moet bewegen, in dit geval omhoog.
# Zoals je ziet eindigt de instructie met twee haakjes. Hiermee vertellen we het programma dat ie de code moet uitvoeren waar we naar wijzen.
# Als we de haakjes niet toevoegen wordt de code niet uitgevoerd, dus vergeet ze niet.
# Om alle onderdelen en beweegrichtingen van de robotarm te zijn kun je in de balk bovenaan het venster kijken onder aangesloten devices->robotArm.
arm.shoulder.up()

# Hier roepen we de sleep functie van de time library aan.
# Zoals je ziet staat er nu iets tussen de haakjes aan het eind van de regel.
# Deze functie laat het programma een aangegeven aantal seconden wachten. In ons geval is dit dus een halve seconde.
# Terwijl het programma wacht blijft de schouder van de robot omhoog bewegen.
time.sleep(0.5)

# Hier laten we een ander onderdeel van de robot bewegen, de elleboog.
# Zoals je ziet staat er nu ook hier iets tussen de haakjes.
# We geven nu een "argument" mee, een stukje extra informatie.
# Zoals je waarschijnlijk al verwacht had vertellen we de robotarm nu hoeveel kracht hij moet gebruiken.
# Dit is een percentage, dus een getal tussen 0 en 100.
# Als we dit argument niet meegeven gebruikt de robotarm 100% van zijn kracht. We kiezen nu voor 50%.
arm.elbow.down(power=50)

# We laten het programma weer een halve seconde wachten. Als het goed is bewegen de schouder en elleboog nu allebei tegelijk, en de schouder sneller dan de elleboog.
time.sleep(0.5)

# Hier zeggen we dat de schouder en elleboog moeten stoppen met bewegen.
arm.shoulder.off()
arm.elbow.off()

# We zijn nu aan het eind van de code gekomen, dus het programma stopt zichzelf nu.
# Als je zelf je eigen code schrijft, vergeet dan niet om bewegende dingen aan het eind van het programma uit te zetten!
# Als je dat niet doet blijft de robotarm doorbewegen totdat ie niet verder kan en maakt ie een hard klikkend geluid.
# In principe kan de robotarm daar even tegen, maar het is er niet goed voor.
# Het is dan ook zaak om als je die fout maakt de motoren zo snel mogelijk toch uit te zetten, niet alleen vanwege de levensduur van de robotarm, maar ook omdat dit geluid klasgenoten aantrekt die commentaar gaan leveren ;)

