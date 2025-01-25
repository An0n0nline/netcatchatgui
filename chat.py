import socket
import tkinter as tk
from tkinter import simpledialog, messagebox
import threading

# Initialize socket globally
s = None

# Function for the Netcat Chat
def netcat_chat_gui():
    def send_message():
        """Handles sending messages to the connected socket."""
        global s
        # Check if the socket is connected before sending
        if s is not None and s.fileno() != -1:  # Ensure the socket is valid and connected
            message = message_entry.get()
            if message:
                # Insert the sent message into the chat box
                chat_box.config(state=tk.NORMAL)  # Enable the Text widget for editing
                chat_box.insert(tk.END, f"You: {message}\n")
                chat_box.config(state=tk.DISABLED)  # Disable the Text widget after insertion
                chat_box.yview(tk.END)  # Scroll to the bottom
                
                s.send(message.encode())  # Send the message to the connected socket
                message_entry.delete(0, tk.END)  # Clear the entry field after sending
        else:
            messagebox.showerror("Error", "Socket is not connected!")

    def receive_message():
        """Handles receiving messages from the server or client."""
        global s
        while True:
            try:
                data = s.recv(1024)  # Try to receive data from the socket
                if data:
                    # Insert the received message into the chat box
                    chat_box.config(state=tk.NORMAL)  # Enable the Text widget for editing
                    chat_box.insert(tk.END, f"Other: {data.decode()}\n")
                    chat_box.config(state=tk.DISABLED)  # Disable the Text widget after insertion
                    chat_box.yview(tk.END)  # Scroll to the bottom
                else:
                    break  # Connection closed
            except:
                break  # Handle socket disconnection

    def listen_for_chat():
        """Sets up the server to listen for incoming connections."""
        global s
        ip = "0.0.0.0"  # Listening on all available interfaces
        port = int(port_entry.get())  # Get port from entry field
        messagebox.showinfo("Info", f"Listening for incoming messages on PORT {port}...")
        
        # Initialize server socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((ip, port))
        s.listen(1)  # Only listen for one incoming connection
        conn, addr = s.accept()  # Accept the incoming connection
        s = conn  # Update 's' to the accepted connection
        messagebox.showinfo("Info", f"Connection established with {addr}")
        
        # Start a thread to listen for incoming messages
        threading.Thread(target=receive_message, daemon=True).start()

    def connect_to_chat():
        """Sets up the client to connect to a chat server."""
        global s
        ip = ip_entry.get()  # Get IP from entry field
        if ip:
            port = int(port_entry.get())  # Get port from entry field
            messagebox.showinfo("Info", f"Connecting to {ip} on PORT {port} for chat...")
            
            # Initialize client socket and try to connect
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect((ip, port))  # Try to establish a connection to the server
                messagebox.showinfo("Info", f"Connected to {ip}:{port}")
                threading.Thread(target=receive_message, daemon=True).start()  # Start listening for incoming messages
            except Exception as e:
                messagebox.showerror("Connection Error", f"Error connecting to {ip}:{port} - {e}")

    def on_listen_button_click():
        """Triggered when the user clicks 'Listen'."""
        listen_for_chat()

    def on_connect_button_click():
        """Triggered when the user clicks 'Connect'."""
        connect_to_chat()

    # Set up the main chat window
    chat_window = tk.Tk()
    chat_window.title("Netcat Chat")

    # Chat Box to display messages
    chat_box = tk.Text(chat_window, height=20, width=50, state=tk.DISABLED)
    chat_box.pack(pady=10)

    # Entry field for message
    message_entry = tk.Entry(chat_window, width=50)
    message_entry.pack(pady=5)

    send_button = tk.Button(chat_window, text="Send", command=send_message)
    send_button.pack(pady=5)

    # Create IP and PORT entry fields
    ip_label = tk.Label(chat_window, text="Enter the server IP address:")
    ip_label.pack(pady=5)
    ip_entry = tk.Entry(chat_window, width=50)
    ip_entry.pack(pady=5)

    port_label = tk.Label(chat_window, text="Enter the PORT number:")
    port_label.pack(pady=5)
    port_entry = tk.Entry(chat_window, width=50)
    port_entry.pack(pady=5)

    # Buttons to start listen or connect
    listen_button = tk.Button(chat_window, text="Listen for Incoming Chat", command=on_listen_button_click)
    listen_button.pack(pady=5)

    connect_button = tk.Button(chat_window, text="Connect to Chat Server", command=on_connect_button_click)
    connect_button.pack(pady=5)

    chat_window.mainloop()

# Main entry point
if __name__ == "__main__":
    netcat_chat_gui()
