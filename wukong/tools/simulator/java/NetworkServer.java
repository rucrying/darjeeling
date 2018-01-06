import java.net.*; 
import java.io.*; 
import java.util.*;

// protocol
// s->c [42]
// c->s 1 byte mode
// if mode==MODE_MESSAGE
//   c->s/s->c 1 byte length, 2 byte LE src 2 byte LE dest, length-5 bytes payload
// if mode==MODE_DISCOVERY
//   s->c      2 byte length, (length-2/2) times 2 byte LE client id

public class NetworkServer extends Thread
{
	private static boolean serverContinue = true;
	private static Map<Integer, NetworkServerClientHandler> clients;
	private static List<INetworkServerMessagesListener> listeners;

	private final int MODE_MESSAGE = 1;
	private final int MODE_DISCOVERY = 2;

	public static void main(String[] args) throws IOException 
	{
		NetworkServer s = new NetworkServer();
		s.addMessagesListener(new StandardOutputListener());
		s.run();
	}

	public NetworkServer() {
		this.listeners = new ArrayList<INetworkServerMessagesListener>();
	}

	public void addMessagesListener(INetworkServerMessagesListener listener) {
		this.listeners.add(listener);
	}

	void fireMessageDropped(int src, int dest, int[] message) {
		for (INetworkServerMessagesListener listener : this.listeners)
			listener.messageDropped(src, dest, message);
	}
	void fireMessageSent(int src, int dest, int[] message) {
		for (INetworkServerMessagesListener listener : this.listeners)
			listener.messageSent(src, dest, message);
	}
	void fireClientConnected(int client) {
		for (INetworkServerMessagesListener listener : this.listeners)
			listener.clientConnected(client);
	}
	void fireClientDisconnected(int client) {
		for (INetworkServerMessagesListener listener : this.listeners)
			listener.clientDisconnected(client);
	}
	void fireDiscovery(Integer[] clients) {
		for (INetworkServerMessagesListener listener : this.listeners)
			listener.discovery(clients);
	}

	public Set<Integer> getConnectedClients() {
		return NetworkServer.clients.keySet();
	}

	private static class StandardOutputListener implements INetworkServerMessagesListener {
		public void messageDropped(int src, int dest, int[] message){
			System.out.println("Dropped message from " + src + " to " + dest + ", length " + message.length);
		}
		public void messageSent(int src, int dest, int[] message){
			System.out.print("Forwarding message from " + src + " to " + dest + "   ");
			for (int i=0; i<message[0]; i++) {
				System.out.print(" [" + String.format("%02X ", message[i]) + "]");
			}
			System.out.println("");
		}
		public void clientConnected(int client){
			System.out.println("Node " + client + " connected.");
		}
		public void clientDisconnected(int client){
			System.out.println("Node " + client + " disconnected.");
		}
		public void discovery(Integer[] ids) {
			System.out.print("Discovery: " + ids.length + " clients (");
			for (int i=0; i<ids.length; i++) {
				System.out.print(ids[i].toString());
				if (i != ids.length-1)
					System.out.print(", ");
			}
			System.out.println(")");
		}
	}

	public void run() {
		clients = new HashMap<Integer, NetworkServerClientHandler>();

		ServerSocket serverSocket = null; 

		try { 
			serverSocket = new ServerSocket(10008); 
			System.out.println ("Connection Socket Created");
			try { 
				while (serverContinue) {
					serverSocket.setSoTimeout(10000);
					try {
						new NetworkServerClientHandler(serverSocket.accept()); 
					}
					catch (SocketTimeoutException ste) {
//						System.out.println ("Timeout Occurred");
					}
				}
			} 
			catch (IOException e) { 
				System.err.println("Accept failed."); 
				System.exit(1); 
			} 
		} 
		catch (IOException e) { 
			System.err.println("Could not listen on port: 10008."); 
			System.exit(1); 
		} 
		finally {
			try {
				System.out.println ("Closing Server Connection Socket");
				serverSocket.close(); 
			}
			catch (IOException e) {
				System.err.println("Could not close port: 10008."); 
				System.exit(1); 
			} 
		}
	}

	private class NetworkServerClientHandler extends Thread {
		public Socket clientSocket;
		public BufferedInputStream in;
		public BufferedOutputStream out;
		public int clientId = 0;
		public boolean keepRunning;

		public NetworkServerClientHandler (Socket clientSoc)
		{
			keepRunning = true;
			clientSocket = clientSoc;
			try {
				clientSocket.setSoTimeout(1000);
			}
			catch (SocketException e) {
				System.err.println("Could not set timeout for socket."); 
				System.exit(1); 
			}
			try {
				in = new BufferedInputStream(clientSocket.getInputStream());
				out = new BufferedOutputStream(clientSocket.getOutputStream());
			}
			catch (IOException e) {
				System.err.println("Could not create input/output streams."); 
				System.exit(1); 
			}
			start();
		}

		public void run()
		{
			try {
				// Say hi
				out.write(42);
				out.flush();

				// Get client mode
				int mode = in.read();

				if (mode == MODE_MESSAGE)
					handle_mode_message(in, out);
				else if (mode == MODE_DISCOVERY)
					handle_mode_discovery(in, out);
				else
					System.out.println("Unknown mode " + mode);
			} 
			catch (IOException e) { 
				System.err.println("Problem with Communication Server");
				System.err.println(e);
				e.printStackTrace(new PrintStream(System.err));
			} 
			finally {
				if (NetworkServer.clients.get(this.clientId) == this)
					NetworkServer.clients.remove(this.clientId);			
			}
		}

		private void handle_mode_message(BufferedInputStream in, BufferedOutputStream out) throws IOException {
			// Get client id
			this.clientId = in.read();
			if (this.clientId < 0)
				throw new IOException("No ID received");
			this.clientId += in.read() << 8;
			this.clientId += in.read() << 16;
			this.clientId += in.read() << 24;
			fireClientConnected(this.clientId);

			if (NetworkServer.clients.get(this.clientId) != null)
				NetworkServer.clients.get(this.clientId).keepRunning = false; // Kill old thread for client with same ID if it was still around
			// Register this client in the global list
			NetworkServer.clients.put(this.clientId, this);

			while(keepRunning) {
				int length = 0;

				try {
					length = in.read();
				}
				catch (SocketTimeoutException ste) {
					continue;
				}

				if (length < 0) {
					// Connection closed
					keepRunning = false;
				} else if (length > 0) {
					// Length byte received.
					if (length < 9) {
						System.out.println("Message with length " + length + " ignored. (length should be >= 9)");
					} else {
						// Process the rest of the message
						int [] message = new int[length];
						message[0] = length;
						for (int i=1; i<length; i++)
							message[i] = in.read();
						int destId = message[5] + (message[6] << 8) + (message[7] << 16) + (message[8] << 24);


						NetworkServerClientHandler destClient = NetworkServer.clients.get(destId);
						if (destClient != null) {
							fireMessageSent(this.clientId, destId, message);
							destClient.sendMessage(message);
						}
						else {
							fireMessageDropped(this.clientId, destId, message);
						}
					}
				}
			}
			fireClientDisconnected(this.clientId);
		}

		private synchronized void sendMessage(int[] message) {
			try {
				for (int i=0; i<message[0]; i++) {
					out.write(message[i]);
				}
				out.flush();
			}
			catch (IOException e) {
				System.err.println("IOException sending message to node " + this.clientId); 
				System.err.println(e);
				this.keepRunning = false;
			}
		}

		private void handle_mode_discovery(BufferedInputStream in, BufferedOutputStream out) throws IOException {
			int number_of_clients = NetworkServer.clients.keySet().size();
			int length = 2+number_of_clients*4;
			System.out.println("discovery, number of clients " + number_of_clients);
			out.write(length%256);
			out.write(length/256);
			Integer[] ids = NetworkServer.clients.keySet().toArray(new Integer[0]);
			fireDiscovery(ids);
			for (int i=0; i<number_of_clients; i++) {
				System.out.println("clients " + ids[i]);
				out.write((ids[i] & 0xFF));
				out.write(((ids[i] >> 8) & 0xFF));
				out.write(((ids[i] >> 16) & 0xFF));
				out.write(((ids[i] >> 24) & 0xFF));
			}
			out.flush();
		}
	}
}
