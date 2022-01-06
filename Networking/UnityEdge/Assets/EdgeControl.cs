using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using System;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.Text;

public class Server
{
    public string address = "";
    public int port = 0;
    public int mtu = 0;
    public bool running = false;
    public bool verbose = false;

    private Thread thread = null;
    private Socket socket = null;

    public Server(string Address, int Port)
    {
        address = Address;
        port = Port;
        mtu = 1500;
        running = false;
        verbose = false;
    }

    public void Run()
    {
        if ((thread == null) || ((thread != null) && (!thread.IsAlive)))
        {
            running = true;
            thread = new Thread(Procedure);
            thread.Start();
        }
        if (running == false) { Stop(); }
    }

    public void Stop()
    {
        if (verbose) { Debug.Log("Stopping Server"); }
        running = false;
        thread.Join();
    }

    private void Reconnect()
    {
        if (verbose) { Debug.Log("Reconnecting Server"); }
        try
        {
            IPAddress addr = IPAddress.Any;
            IPAddress.TryParse(address, out addr);
            IPEndPoint Host = new IPEndPoint(addr, port);
            socket = new Socket(Host.AddressFamily, SocketType.Stream, ProtocolType.Tcp);
            socket.SetSocketOption(SocketOptionLevel.Socket, SocketOptionName.ReuseAddress, true);
            socket.SetSocketOption(SocketOptionLevel.Socket, SocketOptionName.SendTimeout, 1000);
            socket.SetSocketOption(SocketOptionLevel.Socket, SocketOptionName.ReceiveTimeout, 1000);
            socket.Bind(Host);
            socket.Listen(1);
        }
        catch (Exception error)
        {
            if (verbose) { Debug.Log(error); }
            socket = null;
        }
    }

    private void Procedure()
    {
        while (running)
        {
            try
            {
                if (socket == null) { Reconnect(); return; }
                Socket client = socket.Accept();
                if (client != null)
                {
                    string request = "";
                    byte[] buffer = new byte[mtu];
                    client.Receive(buffer, 0, mtu, SocketFlags.None);
                    request = Encoding.UTF8.GetString(buffer);
                    if (verbose) { Debug.Log(request); }

                    //Check and Evaluate Request within Unity
                    //Produce and Validate a Response to the Client
                    string json = "{ \"message\": \"Hello From Unity!\" }";
                    string length = json.Length.ToString();

                    string response = "HTTP/1.1 200 OK\r\n"
                                    + "Content-Type: application/json\r\n"
                                    + "Content-Length: " + length + "\r\n"
                                    + "\r\n" + json + "\r\n";
                    if (verbose) { Debug.Log(response); }

                    buffer = new byte[mtu];
                    buffer = Encoding.UTF8.GetBytes(response);
                    client.Send(buffer, 0, buffer.Length, SocketFlags.None);
                    client.Close();
                }
            }
            catch (Exception error)
            {
                if (verbose) { Debug.Log(error); }
                if (socket != null) { socket.Close(); socket = null; }
                Thread.Sleep(1000);
            }
        }
        socket.Close();
    }
};

public class EdgeControl : MonoBehaviour
{
    private Server server = null;

    void Update()
    {
        if (server != null) { server.Run(); }
        else { server = new Server("0.0.0.0", 10000); server.verbose = true; }
    }

    void OnApplicationQuit()
    {
        if (server != null) { server.Stop(); }
    }
}
