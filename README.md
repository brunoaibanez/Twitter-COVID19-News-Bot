# Hack covid from home 

With the aim to give a useful tool to select relevant COVID-19 information, we develop a streaming tweet filtering engine.

We apply data analysis techniques and storage systems such as streaming processing (Spark-Streaming), artificial intelligence (Natural Language Processing) and non-relational databases (MongoDB). To gather all data and feed our operating system we used the Twitter Developers' API. We worked with conversational software (auditory and textual methods) for the user interface. Everything was deployed and orchestrated on the cloud.

Hack Covid From Home --> https://lnkd.in/gRhekgx

## Veracidad en tiempos de coronavirus

En estos tiempos de cuarentena no paran de llegar rumores de todo tipo. Hemos querido hacer nuestra pequeña contribución al respecto e intentar aportar un poco de rigor a toda la (des)información que nos llega.

El sistema se basa en la interacción de un usuario con un bot de telegram.


![diagram](/img/hack_covid.png)

Nada más entrar, se encuentra con el siguiente menú:

![initial_menu](/img/menu.jpeg)

Las opciones existentes son:

* Recibir las 10 noticias más recientes, importantes y fiables del momento. 

* Recibir en streaming, constantemente las noticias sobre la situación del virus.

* Validar/Desmentir bulos. Debido al gran número de mensajes erróneos que llegan estos días, hemos considerado oportuno y apropiado implementar una opción para que los expertos puedan verificar o desmentir una información que se les ha hecho llegar por diferentes canales.

![validacion](/img/validacion.jpeg)

Al acabar la conversación, se le enviará al usuario un pequeño report sobre su contribución al sistema:

![report](/img/report.jpeg)

Ejemplo de streaming news:

![c1](/img/c1.jpeg)

![c2](/img/c2.jpeg)
