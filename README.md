# 🔐 Proyecto Caso de Estudio – Cifrado Polimórfico

Este proyecto implementa un *algoritmo de cifrado polimórfico de 64 bits* basado en el artículo “Cryptography model to secure IoT device endpoints, based on polymorphic cipher OTP”.  
El objetivo es asegurar la comunicación entre dispositivos IoT mediante el uso de *claves dinámicas* y funciones reversibles de cifrado/descifrado.

---

##  Flujo de Operación

1. *Generación de claves*  
   - Se generan *8 claves de 64 bits* a partir de tres parámetros iniciales: P, Q y S.  

2. *Selección de PSN (Pseudo-random Sequence Number)*  
   - Para cada mensaje se selecciona un valor en el rango *0 – 15*, el cual define el orden de las funciones de cifrado.  

3. *División en bloques*  
   - El texto se divide en *bloques de 8 bytes (64 bits)* para su procesamiento.  

4. *Cifrado*  
   - Cada bloque pasa por *4 funciones reversibles* (f1, f2, f3, f4).  
   - El orden de aplicación depende del valor de PSN.  

5. *Descifrado*  
   - Se aplican las *funciones inversas* (f1_inv, f2_inv, f3_inv, f4_inv).  
   - El orden es exactamente el inverso al usado durante el cifrado, garantizando la recuperación del mensaje original.
