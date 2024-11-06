import tkinter as tk
from tkinter import ttk
import socket
import threading
import json

# Classe principale de l'application MQTT Explorer
class MQTTExplorer:
    def __init__(self, root):
        # Initialisation de l'application
        self.root = root
        self.root.title("MQTT Explorer")  # Titre de la fenêtre
        self.socket = None  # Variable pour stocker la socket de connexion
        self.is_connected = False  # Variable pour indiquer si on est connecté au broker MQTT

        # Création des widgets de l'interface utilisateur
        self.create_widgets()

    def create_widgets(self):
        # Création du notebook qui contient les différents onglets
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # Création des onglets: Subscribe, Publish, et Log
        self.subscribe_tab = ttk.Frame(self.notebook)
        self.publish_tab = ttk.Frame(self.notebook)
        self.log_tab = ttk.Frame(self.notebook)

        # Ajout des onglets au notebook
        self.notebook.add(self.subscribe_tab, text="Subscribe")
        self.notebook.add(self.publish_tab, text="Publish")
        self.notebook.add(self.log_tab, text='Log')

        # --- Onglet Subscribe ---
        # Label et champ de texte pour entrer le topic à s'abonner
        self.subscribe_label = ttk.Label(self.subscribe_tab, text="Topic:")
        self.subscribe_label.pack()

        self.subscribe_entry = ttk.Entry(self.subscribe_tab, width=40)
        self.subscribe_entry.pack()

        # Bouton pour s'abonner à un topic
        self.subscribe_button = ttk.Button(self.subscribe_tab, text="Subscribe", command=self.subscribe_callback)
        self.subscribe_button.pack()

        # Zone de texte pour afficher les messages reçus
        self.subscribe_text = tk.Text(self.subscribe_tab, width=40, height=10)
        self.subscribe_text.pack()

        # Bouton pour exporter le log (messages reçus)
        self.export_log_button = ttk.Button(self.subscribe_tab, text="Export Log", command=self.export_log)
        self.export_log_button.pack()

        # --- Onglet Publish ---
        # Label et champ de texte pour entrer le topic où publier
        self.publish_label = ttk.Label(self.publish_tab, text="Topic:")
        self.publish_label.pack()

        self.publish_entry = ttk.Entry(self.publish_tab, width=40)
        self.publish_entry.pack()

        # Label et champ de texte pour entrer le message à publier
        self.publish_message_label = ttk.Label(self.publish_tab, text="Message:")
        self.publish_message_label.pack()

        self.publish_message_entry = ttk.Entry(self.publish_tab, width=40)
        self.publish_message_entry.pack()

        # Bouton pour publier le message sur le topic spécifié
        self.publish_button = ttk.Button(self.publish_tab, text="Publish", command=self.publish_callback)
        self.publish_button.pack()

        # --- Onglet Log ---
        # Label et zone de texte pour afficher et consulter le log des actions
        self.log_label = ttk.Label(self.log_tab, text="Log:")
        self.log_label.pack()

        self.log_text = tk.Text(self.log_tab, width=40, height=10)
        self.log_text.pack()

        # Bouton pour afficher les logs dans l'onglet Log
        self.log_button = ttk.Button(self.log_tab, text="Afficher Log", command=self.get_log)
        self.log_button.pack()

        # --- Section de connexion au Broker MQTT ---
        # Label et champ de texte pour entrer l'adresse du broker
        self.broker_label = ttk.Label(self.root, text="Broker (IP:Port):")
        self.broker_label.pack()

        self.broker_entry = ttk.Entry(self.root, width=40)
        self.broker_entry.pack()
        self.broker_entry.insert(0, "test.mosquitto.org:1883")  # Valeur par défaut du broker

        # Bouton pour se connecter au broker MQTT
        self.connect_button = ttk.Button(self.root, text="Connect to Broker", command=self.connect_to_broker)
        self.connect_button.pack()

    def connect_to_broker(self):
        # Fonction pour se connecter au broker MQTT
        broker = self.broker_entry.get()  # Récupère l'adresse IP et le port du broker
        host, port = broker.split(":")  # Sépare l'adresse IP et le port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crée une socket TCP
        try:
            # Tentative de connexion au broker
            self.socket.connect((host, int(port)))
            self.is_connected = True  # Met à jour l'état de la connexion
            # Lancement d'un thread pour recevoir les messages en continu
            threading.Thread(target=self.receive_messages, daemon=True).start()
            self.subscribe_text.insert(tk.END, "Connected to broker\n")  # Affiche un message dans l'interface
        except Exception as e:
            # Si la connexion échoue, affiche l'erreur dans l'interface
            self.subscribe_text.insert(tk.END, f"Failed to connect: {e}\n")

    def receive_messages(self):
        # Fonction qui reçoit les messages du broker en continu
        while self.is_connected:
            try:
                # Récupère les données envoyées par le broker
                data = self.socket.recv(1024)
                if data:
                    # Si des données sont reçues, affiche-les dans la zone de texte
                    self.subscribe_text.insert(tk.END, f"Received: {data}\n")
            except:
                break

    def subscribe_callback(self):
        # Fonction appelée lorsqu'on clique sur le bouton "Subscribe"
        topic = self.subscribe_entry.get()  # Récupère le topic à s'abonner
        self.send_mqtt_packet("SUBSCRIBE", topic)  # Envoie un paquet MQTT pour s'abonner
        self.subscribe_text.insert(tk.END, f"Subscribed to {topic}\n")  # Affiche le message dans l'interface

    def publish_callback(self):
        # Fonction appelée lorsqu'on clique sur le bouton "Publish"
        topic = self.publish_entry.get()  # Récupère le topic de publication
        message = self.publish_message_entry.get()  # Récupère le message à publier
        self.send_mqtt_packet("PUBLISH", topic, message)  # Envoie un paquet MQTT pour publier
        self.subscribe_text.insert(tk.END, f"Published to {topic}: {message}\n")  # Affiche le message dans l'interface

    def send_mqtt_packet(self, packet_type, topic, message=None):
        # Fonction pour envoyer un paquet MQTT au broker
        if not self.is_connected:
            self.subscribe_text.insert(tk.END, "Not connected to broker.\n")
            return
        
        # Construction du paquet MQTT à envoyer
        packet = bytearray()
        packet.append(0x10)  # Type de paquet (ici PUBLISH ou SUBSCRIBE)
        packet.append(len(topic) + 2)  # Longueur du paquet
        packet.extend(topic.encode())  # Encode le topic en bytes et l'ajoute au paquet
        if message:
            packet.extend(message.encode())  # Si un message est fourni, l'ajoute au paquet
        packet.append(0x00)  # Null terminator pour la fin du paquet

        # Envoie du paquet via la socket
        self.socket.send(packet)

    def export_log(self):
        # Fonction pour exporter le log (messages reçus) vers un fichier
        log_data = self.subscribe_text.get("1.0", tk.END).strip()  # Récupère tout le texte du log
        if log_data:
            # Sauvegarde le log dans un fichier texte
            with open("mqtt_log.txt", "w") as txt_file:
                txt_file.write(log_data)
            # Sauvegarde le log dans un fichier JSON
            with open("mqtt_log.json", "w") as json_file:
                json.dump({"log": log_data.split("\n")}, json_file)
            self.subscribe_text.insert(tk.END, "Log exported.\n")  # Affiche un message confirmant l'exportation

    def get_log(self):
        # Fonction pour afficher les logs dans l'onglet Log
        log_data = self.subscribe_text.get("1.0", tk.END).strip()  # Récupère tout le texte du log
        # Efface les données précédentes dans l'onglet Log
        self.log_text.delete("1.0", tk.END)
        # Affiche les nouveaux logs dans l'onglet Log
        self.log_text.insert(tk.END, log_data)

    def run(self):
        # Lancement de l'interface graphique Tkinter
        self.root.mainloop()

# Si ce fichier est exécuté directement
if __name__ == "__main__":
    root = tk.Tk()  # Crée une fenêtre principale
    app = MQTTExplorer(root)  # Crée une instance de l'application MQTTExplorer
    app.run()  # Démarre la boucle principale de l'application
