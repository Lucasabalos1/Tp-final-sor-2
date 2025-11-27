import os
import sys
import warnings
import subprocess
import pickle
import tensorflow as tf
import numpy as np
import pandas as pd
from netfilterqueue import NetfilterQueue
from scapy.all import IP, TCP, UDP, ICMP
import requests


BACKEND_URL = "http://192.168.1.20:5000/api/alert"


warnings.filterwarnings("ignore")


try:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


    os.chdir(SCRIPT_DIR)
except NameError:
    print("Error al determinar la ruta del script")
    sys.exit()


try:
    with open('scaler.pkl', 'rb') as f:
        scaler_objeto = pickle.load(f)
    print("Se cargo el scaler de forma correcta")
except FileNotFoundError:
    print("Error: No se encontro el 'scaler.pkl'")
    exit()




try:
    model = tf.keras.models.load_model("lstm_ids_model.h5")
    print("Modelo LSTM cargado correctamente")
except FileNotFoundError:
    print(f"Error: No se encontro el 'lstm_ids_model.h5'")
    exit()


#model.summary()


TIME_STEPS = 20
NUM_FEATURES = model.input_shape[2]
FEATURE_BUFFERS = {}
CATEGORICAL_COLS = ['proto','service','state']
ALL_FEATURE_COLUMNS = ['dur', 'spkts', 'dpkts', 'sbytes', 'dbytes', 'rate', 'sttl', 'dttl', 'sload', 'dload', 'sloss', 'dloss', 'sinpkt', 'dinpkt', 'sjit', 'djit', 'swin', 'stcpb', 'dtcpb', 'dwin', 'tcprtt', 'synack', 'ackdat', 'smean', 'dmean', 'trans_depth', 'response_body_len', 'ct_srv_src', 'ct_state_ttl', 'ct_dst_ltm', 'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'ct_src_ltm', 'ct_srv_dst', 'proto_a/n', 'proto_aes-sp3-d', 'proto_any', 'proto_argus', 'proto_aris', 'proto_arp', 'proto_ax.25', 'proto_bbn-rcc', 'proto_bna', 'proto_br-sat-mon', 'proto_cbt', 'proto_cftp', 'proto_chaos', 'proto_compaq-peer', 'proto_cphb', 'proto_cpnx', 'proto_crtp', 'proto_crudp', 'proto_dcn', 'proto_ddp', 'proto_ddx', 'proto_dgp', 'proto_egp', 'proto_eigrp', 'proto_emcon', 'proto_encap', 'proto_etherip', 'proto_fc', 'proto_fire', 'proto_ggp', 'proto_gmtp', 'proto_gre', 'proto_hmp', 'proto_i-nlsp', 'proto_iatp', 'proto_ib', 'proto_idpr', 'proto_idpr-cmtp', 'proto_idrp', 'proto_ifmp', 'proto_igmp', 'proto_igp', 'proto_il', 'proto_ip', 'proto_ipcomp', 'proto_ipcv', 'proto_ipip', 'proto_iplt', 'proto_ipnip', 'proto_ippc', 'proto_ipv6', 'proto_ipv6-frag', 'proto_ipv6-no', 'proto_ipv6-opts', 'proto_ipv6-route', 'proto_ipx-n-ip', 'proto_irtp', 'proto_isis', 'proto_iso-ip', 'proto_iso-tp4', 'proto_kryptolan', 'proto_l2tp', 'proto_larp', 'proto_leaf-1', 'proto_leaf-2', 'proto_merit-inp', 'proto_mfe-nsp', 'proto_mhrp', 'proto_micp', 'proto_mobile', 'proto_mtp', 'proto_mux', 'proto_narp', 'proto_netblt', 'proto_nsfnet-igp', 'proto_nvp', 'proto_ospf', 'proto_pgm', 'proto_pim', 'proto_pipe', 'proto_pnni', 'proto_pri-enc', 'proto_prm', 'proto_ptp', 'proto_pup', 'proto_pvp', 'proto_qnx', 'proto_rdp', 'proto_rsvp', 'proto_rvd', 'proto_sat-expak', 'proto_sat-mon', 'proto_sccopmce', 'proto_scps', 'proto_sctp', 'proto_sdrp', 'proto_secure-vmtp', 'proto_sep', 'proto_skip', 'proto_sm', 'proto_smp', 'proto_snp', 'proto_sprite-rpc', 'proto_sps', 'proto_srp', 'proto_st2', 'proto_stp', 'proto_sun-nd', 'proto_swipe', 'proto_tcf', 'proto_tcp', 'proto_tlsp', 'proto_tp++', 'proto_trunk-1', 'proto_trunk-2', 'proto_ttp', 'proto_udp', 'proto_unas', 'proto_uti', 'proto_vines', 'proto_visa', 'proto_vmtp', 'proto_vrrp', 'proto_wb-expak', 'proto_wb-mon', 'proto_wsn', 'proto_xnet', 'proto_xns-idp', 'proto_xtp', 'proto_zero', 'service_dhcp', 'service_dns', 'service_ftp', 'service_ftp-data', 'service_http', 'service_irc', 'service_pop3', 'service_radius', 'service_smtp', 'service_snmp', 'service_ssh', 'service_ssl', 'state_CLO', 'state_CON', 'state_FIN', 'state_INT', 'state_REQ', 'state_RST']


NUMERIC_BASE_FEATURES = [ 'dur', 'spkts', 'dpkts', 'sbytes', 'dbytes', 'rate', 'sttl', 'dttl', 'sload', 'dload', 'sloss',
                        'dloss', 'sinpkt', 'dinpkt', 'sjit', 'djit', 'swin', 'stcpb', 'dtcpb', 'dwin', 'tcprtt', 'synack',
                        'ackdat', 'smean', 'dmean', 'trans_depth', 'response_body_len', 'ct_srv_src', 'ct_state_ttl', 'ct_dst_ltm',
                        'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'ct_src_ltm', 'ct_srv_dst' ]


def extract_realtime_features(scapy_packet):
    try:


        protocolo = '0'
        estado = 'INT'
        servicio = '-'
        sbytes = 0


        if not scapy_packet.haslayer(IP):
            return None
       
        protocolo = str(scapy_packet[IP].proto)
        sbytes = len(scapy_packet)


        if scapy_packet.haslayer(TCP):
            protocolo = 'tcp'


            if scapy_packet[TCP].flags & 0x02:
                estado = 'REQ'
            elif scapy_packet[TCP].flags & 0x01:
                estado = 'FIN'
            elif scapy_packet[TCP].flags & 0x04:
                estado = 'RST'
           
            dport = scapy_packet[TCP].dport
            if dport == 80: servicio = 'http'
            elif dport == 443: servicio = 'ssl'
            elif dport == 21: servicio = 'ftp'


        elif scapy_packet.haslayer(UDP):
            protocolo = 'udp'
            if scapy_packet[UDP].dport == 53: servicio = 'dns'


        elif scapy_packet.haslayer(ICMP):
            protocolo = 'icmp'
            estado = 'CON'
           


        datos_paquete = {feat: 0.0 for feat in NUMERIC_BASE_FEATURES}


        datos_paquete['sbytes'] = sbytes
        datos_paquete['dur'] = 0.000001
        datos_paquete['rate'] = 10.0
        datos_paquete['sttl'] = scapy_packet[IP].ttl


        datos_paquete['proto'] = protocolo
        datos_paquete['service'] = servicio
        datos_paquete['state'] = estado


        df_paquete = pd.DataFrame([datos_paquete])
        df_ohe = pd.get_dummies(df_paquete, columns=CATEGORICAL_COLS)


        df_final = pd.DataFrame(columns=ALL_FEATURE_COLUMNS)
        df_final = pd.concat([df_final, df_ohe], ignore_index=True)
        df_final.fillna(0, inplace=True)
        df_final = df_final[ALL_FEATURE_COLUMNS]


        df_final.replace([np.inf, -np.inf], np.nan, inplace=True)
        df_final.fillna(0, inplace=True)


        return df_final.values
    except Exception as e:
        print(f"No se pudo extraer features del paquete: {e}")
        return None


def create_sequence_for_interface(features_normalizadas, src_ip):
    if features_normalizadas is None:
        return None


    if features_normalizadas.ndim == 1:
        features_normalizadas = features_normalizadas.reshape(1,-1)


    current_feature_list = features_normalizadas[0].tolist()


    buf = FEATURE_BUFFERS.get(src_ip)
    if buf is None:
        buf = []
        FEATURE_BUFFERS[src_ip] = buf


    buf.append(current_feature_list)


    if len(buf) > TIME_STEPS:
        buf.pop(0)


    if len(buf) < TIME_STEPS:
        return None


    X_seq_2d = np.array(buf)
    X_seq_3d = X_seq_2d.reshape(1, TIME_STEPS, X_seq_2d.shape[1])
    return X_seq_3d




def implement_containment(src_ip):


    payload = {
        "ip": src_ip,
        "status": "BLOQUEADO"
    }

    try:
        resp = requests.post(BACKEND_URL, json=payload, timeout=2)

        print(f"[HTTP] POST → Status {resp.status_code}")


        try:
            print("[HTTP] Body:", resp.json())
        except:
            print("[HTTP] Raw:", resp.text)


    except requests.exceptions.RequestException as e:
        print(f"Fallo al enviar la alerta: {e}")


    check_cmd = f"sudo iptables -C INPUT -s {src_ip} -j DROP"
    add_cmd   = f"sudo iptables -A INPUT -s {src_ip} -j DROP"


    try:
        result = subprocess.run(check_cmd, shell=True)

        if result.returncode != 0:
            subprocess.run(add_cmd, shell=True, check=True)
            print(f"IP {src_ip} bloqueada permanentemente via iptables.")
        else:
            print(f"IP {src_ip} ya estaba bloqueada (no se duplica la regla).")


    except subprocess.CalledProcessError as e:
        print(f"No se pudo bloquear la IP {src_ip}: {e}")

def process_packet(paquete):
    try:
        scapy_packet = IP(paquete.get_payload())


        features_2d = extract_realtime_features(scapy_packet)
        if features_2d is None:
            paquete.accept()
            return


        try:
            features_normalizados = scaler_objeto.transform(features_2d)
        except Exception as e:
            print(f"Error al normalizar features: {e}")
            paquete.accept()
            return


        src_ip = scapy_packet[IP].src
        X_seq_3d = create_sequence_for_interface(features_normalizados, src_ip)


        if X_seq_3d is not None:
            prediccion = model.predict(X_seq_3d, verbose=0)
            clase_predicha = np.argmax(prediccion)
            #print(f"[DEBUUG] IP: {scapy_packet[IP].src}, Prediccion: {clase_predicha}")


            if clase_predicha == 1:
                print(f"Paquete de {scapy_packet[IP].src} BLOQUEADO")
                implement_containment(scapy_packet[IP].src)
                paquete.drop()
                return


    except Exception as e:
        print(f"Ocurrio un error al procesar el paquete:{e}")
    paquete.accept()


def run_nfqueue():
    nfqueue = None
    try:
        nfqueue = NetfilterQueue()
        nfqueue.bind(0, process_packet)
        print("Conexion a NFQUEUE establecida, esperando trafico....")
        nfqueue.run()
    except Exception as e:
        print(f"Fallo al conectar o iniciar NFQUEUE: {e}")
    finally:
        print("Desvinvulando NFQUEUE. Restaurando flujo de trafico...")
        if nfqueue is not None:
            try:
                nfqueue.unbind()
            except Exception:
                pass


if __name__ == '__main__':
    run_nfqueue()

