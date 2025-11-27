from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from enum import Enum
import os 
import datetime


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = F"sqlite:///{os.path.join(basedir, 'instance', 'atacks.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_key_para_pruebas_locales')
CORS(app)
db = SQLAlchemy(app)

class EstadoAlerta(Enum):
    ACEPTADO = "ACEPTADO"
    BLOQUEADO = "BLOQUEADO"

class Alerta(db.Model):
    __tablename__ = "alerta"

    id = db.Column(db.Integer, primary_key=True)
    origin_ip = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default = datetime.datetime.utcnow)
    state = db.Column(db.Enum(EstadoAlerta), nullable=False)


#Creacion de la base de datos
#with app.app_context():
#    db.create_all()
#    print("Base de datos creada con exito")

@app.route("/api/alert", methods=['POST'])
def alert():
    data = request.get_json()

    ip = data.get("ip")
    state = data.get("status")

    if not ip or not state:
        return jsonify({"success": False, "message": "Los campos no pueden estar vacios"}),400
    
    fecha_hora = datetime.datetime.now()

    alert = Alerta(origin_ip = ip,
                   timestamp = fecha_hora, 
                   state = EstadoAlerta(state.upper())
            )
    
    db.session.add(alert)
    db.session.commit()

    return jsonify({"success": True, "message": "La alerta se guardo correctamente"}),201

@app.route("/api/alerts", methods=['GET'])
def get_alerts():
    alertas = Alerta.query.order_by(Alerta.timestamp.desc()).all()

    if not alertas:
        return jsonify({"succes": False, "message": "No hay ninguna alerta registrada en la base de datos"}),404

    alerts = []

    for alert in alertas:
        alerts.append({"id": alert.id, 
                       "ip_origen": alert.origin_ip, 
                       "fecha_hora": alert.timestamp.strftime("%Y-%m-%d %H:%M:%S"), 
                       "estado": alert.state.value})

    return jsonify({"success": True, "data": alerts}),200

@app.route("/api/metrics", methods=['GET'])
def obtain_metrics():
    
    total_alerts = db.session.query(Alerta).count()
    
    blocked_count = db.session.query(Alerta).filter(
        Alerta.state == EstadoAlerta.BLOQUEADO
    ).count()
    
    
    if total_alerts > 0:
        block_success_rate = (blocked_count / total_alerts) * 100
    else:
        block_success_rate = 0.0
    
    metrics = {
        "total_alerts_processed": total_alerts,
        "blocked_attacks_count": blocked_count,
        "block_success_rate": f"{block_success_rate:.2f}%",
        "last_updated": datetime.datetime.now().strftime("%H:%M:%S")
    }
    
    return jsonify({"success": True, "data": metrics}), 200



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)