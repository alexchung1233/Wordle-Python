"""Main executable target"""
import server as server
app = server.get_server()


if __name__ == '__main__':
   app.run()
