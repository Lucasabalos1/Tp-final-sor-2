import tensorflow as tf
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
import numpy as np
from sklearn.metrics import classification_report


TIME_STEPS = 20
NUM_FEATURES = 0
NUM_CLASSES = 2


# Bloque 1: Carga de datos y configuracion
try:
   X_train = np.load('X_train.npy')
   X_test = np.load('X_test.npy')
   y_train = np.load('y_train.npy')
   y_test = np.load('y_test.npy')


   NUM_FEATURES = X_train.shape[2]


   print("Datos cargados con exito")
except FileNotFoundError:
   print("Error: NO se encontraron los archivos .npy")
   exit()


# Bloque 2: Definicion de la arquitectura LSTM


model = Sequential()


model.add(LSTM(units=128, input_shape=(TIME_STEPS, NUM_FEATURES), return_sequences=True))
model.add(Dropout(0.2))


model.add(LSTM(units=64))
model.add(Dropout(0.2))


model.add(Dense(units=NUM_CLASSES, activation='softmax'))


model.summary()


# Bloque 3: Compilacion y entrenamiento


model.compile(
   optimizer='adam',
   loss='categorical_crossentropy',
   metrics=['accuracy']
)


# Entrenamiento


history = model.fit(
   X_train, y_train,
   epochs=10,
   batch_size=256,
   validation_split=0.1,
   shuffle=False
)


# Bloque 4: Evaluacion y serializacion


print("Generando metricas....")
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"Presicion final en datos de prueba:{accuracy*100:.2f}%")


y_pred = model.predict(X_test)
y_pred_classes = np.argmax(y_pred, axis=1)
y_true_classes = np.argmax(y_test, axis=1)


print("Reporte de clasificacion")
print(classification_report(y_true_classes, y_pred_classes, target_names=['Normal (0)', 'Ataque(1)']))


model.save('lstm_ids_model.h5')
print(f"\n[Exito] Modelo entrenado guardado como 'lstm_ids_model.h5'.")
