# Entrenamiento del modelo LSTM

El entrenamiento del modelo RNN/LSTM se realiza en dos pasos secuenciales. Este proceso es necesario para generar los archivos binarios (.h5 y .pkl) que utiliza el sistema en tiempo real.

Advertencia: Se necesitara una VM Linux para poder utilizar este modelo. Este proceso consume altos recursos de CPU y RAM, y puede tardar 30 minutos o más en la VM debido al tamaño del dataset y al uso de la memoria Swap.

## Preparación de recursos

Antes de comenzar, asegúrese de que:

* Crear el .env e instalar las dependencias necesarias

```bash
pip install tensorflow numpy pandas scikit-learn netfilterqueue scapy requests
```

* Se encuentre en el directorio raíz de la aplicación (ej., ~/tpFInal/ids_runtime_engine/).

* El entorno virtual .venv esté activo (source .venv/bin/activate).

* El archivo de datos UNSW_NB15_training-set.csv esté presente en la carpeta archive/



## Preprocesamiento y Feature Engineering

Este script limpia el dataset, aplica la codificación One-Hot Encoding, normaliza las features y las transforma en secuencias 3D.

Ejecutamos el preprocess.py

Archivo generado: 
* sclaler.pkl: Objeto de normalización MinMax
* X_train.npy, X_test.npy, Y_train.npy, Y_test.npy

En la misma ruta una vez ejecutado el script anterior y generados los archivos ahora ejecutamos el train.model.py

Archivos generados:
* lstm_ids_model.h5: Modelo entrenado con los datos y dataset anteriormente generados

Una vez obtenidos el skaler.pkl y el lstm_ids_model.h5 podremos ejecutar el ids_runtime.py

Pero antes en otra terminal debemos de ejecutar las siguientes reglas


```bash
sudo iptables -F
sudo iptables -X

sudo iptables -A INPUT -p tcp --dport 5000 -j ACCEPT   # Backend Flask
sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT


sudo iptables -A INPUT -j NFQUEUE --queue-num 0

sudo iptables -I INPUT -s 127.0.0.1 -d 127.0.0.1 -j ACCEPT

```

Una vez aplicada estas reglas podemos levantar la api y ejecutar el ids_runtime.py

```bash
python app.py
 	
sudo /home/alumno/tpFInal/.venv/bin/python /home/alumno/tpFInal/ids_runtime.py

```
Solo bastara enviar el ataque desde otra VM y ver los resultados, tambien funciona realizando el ataque desde la misma VM


