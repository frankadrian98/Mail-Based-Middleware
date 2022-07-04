# Mail-Based-Middleware

# Integrantes:

Frank Adrian Pérez Morales 411 @frankadrian98 (Github) @cyberneroazzurro (Telegram)

Camilo Rodríguez Velázquez 412 @camilorod4312  (Github) @ErichKrausse (Telegram)

Aldo Javier Verdesia Delgado 512   @Yulii01   (Github) @YulyG01 (Telegram)

# Objetivos:
El objetivo del proyecto es crear un **Midelware** distribuido para conexiones de tipo cliente servidor donde estas se realicen mediante correos electrónicos. 

# Resumen:
El proyecto cuenta de tres estructuras fundamentales las cuales se complementan para la realización de las tareas. Debido a la demanda de las conexiones de forma de correo electrónico se confeccionaron dos servidores uno que tiene definido el protocolo SMTP y la función de enviar mensajes en forma de mail hacia una base de datos para su venidera recuperación. La recuperación de estos mail se basan en un servidor que implementa el protocolo POP-3, recibe una petición después de autentificar al usuario y muestra todos los mensajes de los cuales son destinatario. La información de los mensajes enviados se almacena en un json en la pc, en este se encuentra los usuarios ya confirmados y los mensajes con un receptor definido. Estos datos se replican a través de la utilización de un anillo de Chord el cual va pasando información actualizada a todos los servidores logrando que estos tengan sus mensajes de manera concisa  ordenadas

# Funcionamiento 

Se levantan nodos chord como cantidad de servidores Smtp con el siguiente comando

python chord.py -id 2 -addr 127.0.0.1:5000 -bits 3 

python chord.py -id 2 -addr 127.0.0.1:5002 -bits 3 -entry_addr 127.0.0.1:5000

Esto mantiene los nodos enviándose información y actualizando de manera constante. Al no existir un líder y estar repartida las responsabilidades los nodos no tendrán manera de determinar si su sucesor o antecesor están correctos a menos que los verifique 

# Especificaciones
La implementación del Chord_node.py sigue las ideas ilustradas en el pseudocódigo del artículo: *Chord: A Scalable Peer-to-peer Lookup Service for Internet Applications*. Al cual se le añadió:

- **Tolerancia a fallas:** Cada nodo en la red tiene una lista de `r` sucesores. Cuando un nodo `A` falla, su predecesor `B` buscará en la lista de sucesores un nodo que esté vivo `C`. A continuación, `B` pone como su sucesor a `C` y le notifica que es su predecesor. Al cabo del tiempo la red se estabilizará mediante el método `fix_fingers` cuyo pseudocódigo está en el artículo. Para mantener actualizada la lista de `r` sucesores se implementó un método análogo al `fix_fingers` pero esta vez sobre la lista de sucesores. La búsqueda de `find_predeccesor` ahora toma en cuenta los nodos caídos, y  busca un camino alternativo para encontrar el nodo correspondiente.
- **Replicación**: Cuando un nodo se cae, sus datos asociados a sus keys no se pierden debido a que en anteriores momentos copió sus datos a los nodos sucesores de la lista de `r` sucesores.  Cada cierto tiempo cada nodo le envía los últimos datos almacenados para replicar a uno de los  nodos en su lista de sucesores. Cuando un nodo `A` se va de la red,  su predecesor `B` se da cuenta . El nodo `B` busca en su lista de sucesores  quien es el próximo sucesor vivo `C`, y le envía una  lista que significa que `C` debe encargarse de los datos del nodo `A`. Los  datos del nodo `A` estarán replicados en el nodo `C`, el cual pasará a poseer dichos datos como suyos, incluso para su posterior replicación en sus nodos sucesores.


