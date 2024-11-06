import tkinter as tk
from tkinter import ttk
import socket
import threading
import json

class MQTTExplorer:
    def __init__(self, root):
        self.root = root
        self.root.title("MQTT Explorer")
        self.socket = None
        self.is_connected = False

        # Creation des widgets
        self.create_widgets()

    def create_widgets(self):
        # Notebook avec les onglets "Subscribe" "Publish" et "Log"
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        self.subscribe_tab = ttk.Frame(self.notebook)
        self.publish_tab = ttk.Frame(self.notebook)
        self.log_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.subscribe_tab, text="Subscribe")
        self.notebook.add(self.publish_tab, text="Publish")
        self.notebook.add(self.log_tab, text='Log')

        # Onglet Subscribe
        self.subscribe_label = ttk.Label(self.subscribe_tab, text="Topic:")
        self.subscribe_label.pack()

        self.subscribe_entry = ttk.Entry(self.subscribe_tab, width=40)
        self.subscribe_entry.pack()

        self.subscribe_button = ttk.Button(self.subscribe_tab, text="Subscribe", command=self.subscribe_callback)
        self.subscribe_button.pack()

        self.subscribe_text = tk.Text(self.subscribe_tab, width=40, height=10)
        self.subscribe_text.pack()

        self.export_log_button = ttk.Button(self.subscribe_tab, text="Export Log", command=self.export_log)
        self.export_log_button.pack()

        # Onglet Publish
        self.publish_label = ttk.Label(self.publish_tab, text="Topic:")
        self.publish_label.pack()

        self.publish_entry = ttk.Entry(self.publish_tab, width=40)
        self.publish_entry.pack()

        self.publish_message_label = ttk.Label(self.publish_tab, text="Message:")
        self.publish_message_label.pack()

        self.publish_message_entry = ttk.Entry(self.publish_tab, width=40)
        self.publish_message_entry.pack()

        self.publish_button = ttk.Button(self.publish_tab, text="Publish", command=self.publish_callback)
        self.publish_button.pack()

        # Onglet Log
        self.log_label = ttk.Label(self.log_tab, text="Log:")
        self.log_label.pack()

        self.log_text = tk.Text(self.log_tab, width=40, height=10)
        self.log_text.pack()

        self.log_button = ttk.Button(self.log_tab, text="Afficher Log", command=self.get_log)
        self.log_button.pack()

        # Widget de connection Broker MQTT
        self.broker_label = ttk.Label(self.root, text="Broker (IP:Port):")
        self.broker_label.pack()

        self.broker_entry = ttk.Entry(self.root, width=40)
        self.broker_entry.pack()
        self.broker_entry.insert(0, "test.mosquitto.org:1883")

        self.connect_button = ttk.Button(self.root, text="Connect to Broker", command=self.connect_to_broker)
        self.connect_button.pack()

    def connect_to_broker(self):
        broker = self.broker_entry.get()
        host, port = broker.split(":")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((host, int(port)))
            self.is_connected = True
            threading.Thread(target=self.receive_messages, daemon=True).start()
            self.subscribe_text.insert(tk.END, "Connected to broker\n")
        except Exception as e:
            self.subscribe_text.insert(tk.END, f"Failed to connect: {e}\n")

    def receive_messages(self):
        while self.is_connected:
            try:
                data = self.socket.recv(1024)
                if data:
                    # Processus de reception du message MQTT
                    self.subscribe_text.insert(tk.END, f"Received: {data}\n")
            except:
                break

    def subscribe_callback(self):
        topic = self.subscribe_entry.get()
        self.send_mqtt_packet("SUBSCRIBE", topic)
        self.subscribe_text.insert(tk.END, f"Subscribed to {topic}\n")

    def publish_callback(self):
        topic = self.publish_entry.get()
        message = self.publish_message_entry.get()
        self.send_mqtt_packet("PUBLISH", topic, message)
        self.subscribe_text.insert(tk.END, f"Published to {topic}: {message}\n")

    def send_mqtt_packet(self, packet_type, topic, message=None):
        if not self.is_connected:
            self.subscribe_text.insert(tk.END, "Not connected to broker.\n")
            return
        # Construction du paquet MQTT
        packet = bytearray()
        packet.append(0x10)  # MQTT type de paquet (SUBSCRIBE ou PUBLISH)
        packet.append(len(topic) + 2)  # Longueur du paquet
        packet.extend(topic.encode())  # Topic
        if message:
            packet.extend(message.encode())  # Message
        packet.append(0x00)  # Null terminator

        # Envoi de paquet
        self.socket.send(packet)

    def export_log(self):
        log_data = self.subscribe_text.get("1.0", tk.END).strip()
        if log_data:
            # Export vers un fichier texte
            with open("mqtt_log.txt", "w") as txt_file:
                txt_file.write(log_data)
            # Export vers un fichier JSON
            with open("mqtt_log.json", "w") as json_file:
                json.dump({"log": log_data.split("\n")}, json_file)
            self.subscribe_text.insert(tk.END, "Log exported.\n")

    def get_log(self):
        # Récupérer les données de log depuis la zone de texte de l'onglet Subscribe
        log_data = self.subscribe_text.get("1.0", tk.END).strip()
        #Effacer les données précédentes
        self.log_text.delete("1.0", tk.END)
        #Ajouter les nouveaux logs 
        self.log_text.insert(tk.END, log_data)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = MQTTExplorer(root)
    app.run()
