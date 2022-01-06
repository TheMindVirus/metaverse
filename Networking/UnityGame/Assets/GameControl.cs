using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using System;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.Text;

public class Client
{
    public string address = "";
    public int port = 0;
    public int mtu = 0;
    public bool running = false;
    public bool verbose = false;

    private Thread thread = null;
    private Socket socket = null;

    public Client(string Address, int Port)
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
        if (verbose) { Debug.Log("Stopping Client"); }
        running = false;
        thread.Join();
    }

    private void Reconnect()
    {
        if (verbose) { Debug.Log("Reconnecting Client"); }
        try
        {
            IPAddress addr = IPAddress.Any;
            IPAddress.TryParse(address, out addr);
            IPEndPoint Host = new IPEndPoint(addr, port);
            socket = new Socket(Host.AddressFamily, SocketType.Stream, ProtocolType.Tcp);
            socket.SetSocketOption(SocketOptionLevel.Socket, SocketOptionName.ReuseAddress, true);
            socket.SetSocketOption(SocketOptionLevel.Socket, SocketOptionName.SendTimeout, 1000);
            socket.SetSocketOption(SocketOptionLevel.Socket, SocketOptionName.ReceiveTimeout, 1000);
            socket.Connect(Host);
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
                if (socket != null)
                {
                    string request = "GET / HTTP/1.1\r\n";
                    byte[] buffer = new byte[mtu];
                    buffer = Encoding.UTF8.GetBytes(request);
                    socket.Send(buffer, 0, buffer.Length, SocketFlags.None);
                    if (verbose) { Debug.Log(request); }

                    string response = "";
                    buffer = new byte[mtu];
                    socket.Receive(buffer, 0, mtu, SocketFlags.None);
                    response = Encoding.UTF8.GetString(buffer);
                    if (verbose) { Debug.Log(response); }
                    socket.Close();
                    socket = null;

                    //Process the received data (JSON)
                    //Update the Scene accordingly
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

public class GameControl : MonoBehaviour
{
    private Client client = null;

    void Update()
    {
        if (client != null) { client.Run(); }
        else { client = new Client("127.0.0.1", 10000); client.verbose = true; }
    }

    void OnApplicationQuit()
    {
        if (client != null) { client.Stop(); }
    }
}
