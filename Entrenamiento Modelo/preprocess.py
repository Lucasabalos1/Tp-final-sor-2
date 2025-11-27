import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import pickle
import tensorflow as tf


filepath = "archive/UNSW_NB15_training-set.csv"

df = pd.read_csv(filepath, encoding="latin-1")

if 'ï»¿id' in df.columns:
	df.drop(columns=['ï»¿id'], inplace=True, errors='ignore')
if 'id' in df.columns: 
	df.drop(columns=['id'], inplace=True, errors='ignore')


df.replace([np.inf, -np.inf], np.nan, inplace=True) 
df.fillna(0, inplace=True)

y = df['label']

columnas_a_eliminar = [ "is_sm_ips_ports", "ct_ftp_cmd", "ct_flw_http_mthd", "is_ftp_login", "label", "attack_cat"] 
x = df.drop(columnas_a_eliminar, axis=1)

print(x.dtypes)

columnas_categoricas = x.select_dtypes(include=['object']).columns

print(columnas_categoricas.tolist())

x_codificado = pd.get_dummies(x, columns=columnas_categoricas, drop_first=True)

print(f"\n Lista de columnas finales:")
print(x_codificado.columns.tolist())

print(x_codificado.head())

# Bloque 1: Normalizacion Minmax y guardado del escalador
scaler = MinMaxScaler()

x_normalizado = scaler.fit_transform(x_codificado)

with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

print("\n[Exito] Dataset normalizado y scaler guardado como 'scaler.pkl'.")


# Bloque 2: Creacion de secuencias 3D (formato para LSTM)
TIME_STEPS = 20
NUM_FEATURES = x_normalizado.shape[1]

def create_sequences(X, y, time_steps):
    Xs, ys = [],[]

    for i in range(len(X) - time_steps):
        Xs.append(X[i:(i + time_steps)])
        ys.append(y.iloc[i + time_steps])
    return np.array(Xs), np.array(ys)

X_seq, y_seq = create_sequences(x_normalizado, y, TIME_STEPS)

y_seq_cat = tf.keras.utils.to_categorical(y_seq, num_classes=2)


# Bloque 3: Guardar entregables finales y separa datos

X_train, X_test, y_train, y_test = train_test_split(
    X_seq, y_seq_cat, test_size=0.2, random_state=42
)

np.save('X_train.npy', X_train)
np.save('X_test.npy', X_test)
np.save('y_train.npy', y_train)
np.save('y_test.npy', y_test)

print(f"\n[Exito] Datos de entrenamientos y pruebas guardados")
