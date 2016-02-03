"""
This is the old server
The new server is named ad5764_dcbox.py
"""

# # Copyright []
# #
# # This program is free software: you can redistribute it and/or modify
# # it under the terms of the GNU General Public License as published by
# # the Free Software Foundation, either version 2 of the License, or
# # (at your option) any later version.
# #
# # This program is distributed in the hope that it will be useful,
# # but WITHOUT ANY WARRANTY; without even the implied warranty of
# # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# # GNU General Public License for more details.
# #
# # You should have received a copy of the GNU General Public License
# # along with this program.  If not, see <http://www.gnu.org/licenses/>.

# """
# ### BEGIN NODE INFO
# [info]
# name = DCBOX Arduino
# version = 1.0
# description = DCBOX control
# [startup]
# cmdline = %PYTHON% %FILE%
# timeout = 20
# [shutdown]
# message = 987654321
# timeout = 20
# ### END NODE INFO
# """

# # this is the server name under which devices of this type are stored in the registry.
# global serverNameAD5764_DCBOX; serverNameAD5764_DCBOX = "ad5764_dcbox"

# import platform
# global serial_server_name
# serial_server_name = (platform.node() + "_serial_server").replace("-","_").lower()

# from labrad.server import setting
# from labrad.devices import DeviceServer,DeviceWrapper
# from twisted.internet.defer import inlineCallbacks, returnValue
# import labrad.units as units
# from labrad.types import Value

# TIMEOUT = Value(5,'s')
# BAUD    = 115200

# class AD5764DcboxWrapper(DeviceWrapper):
#     channels = [0,1,2,3,4,5,6,7]

#     @inlineCallbacks
#     def connect(self, server, port):
#         """Connect to a device."""
#         print 'connecting to "%s" on port "%s"...' % (server.name, port),
#         self.server = server
#         self.ctx = server.context()
#         self.port = port
#         p = self.packet()
#         p.open(port)
#         p.baudrate(BAUD)
#         p.read()  # clear out the read buffer
#         p.timeout(TIMEOUT)
#         print(" CONNECTED ")
#         yield p.send()
        
#     def packet(self):
#         """Create a packet in our private context."""
#         return self.server.packet(context=self.ctx)

#     def shutdown(self):
#         """Disconnect from the serial port when we shut down."""
#         return self.packet().close().send()

#     @inlineCallbacks
#     def write(self, code):
#         """Write a data value to the heat switch."""
#         yield self.packet().write(code).send()

#     @inlineCallbacks
#     def read(self):
#         p=self.packet()
#         p.read_line()
#         ans=yield p.send()
#         returnValue(ans.read_line)

#     @inlineCallbacks
#     def query(self, code):
#         """ Write, then read. """
#         p = self.packet()
#         p.write_line(code)
#         p.read_line()
#         ans = yield p.send()
#         returnValue(ans.read_line)

#     @inlineCallbacks
#     def set_voltage(self,channel,voltage):
#         if channel not in self.channels:
#             print("ERROR: invalid channel")
#             raise
#         if abs(voltage)>10.0:
#             print("ERROR: invalid voltage. Must be between -10.0 and 10.0")
#             raise
#         yield self.packet().write("SET,%i,%f\r"%(channel,voltage)).send()
#         p=self.packet()
#         p.read_line()
#         ans = yield p.send()
#         returnValue(ans.read_line)
        


# class AD5764DcboxServer(DeviceServer):
#     name = 'ad5764_dcbox'
#     deviceName = 'Arduino Dcbox'
#     deviceWrapper = AD5764DcboxWrapper

#     channels = [0,1,2,3,4,5,6,7]


#     @inlineCallbacks
#     def initServer(self):
#         print 'loading config info...',
#         self.reg = self.client.registry()
#         yield self.loadConfigInfo()
#         print 'done.'
#         print self.serialLinks
#         yield DeviceServer.initServer(self)

#     @inlineCallbacks
#     def loadConfigInfo(self):
#         reg = self.reg
#         yield reg.cd(['', 'Servers', serverNameAD5764_DCBOX, 'Links'], True)
#         dirs, keys = yield reg.dir()
#         p = reg.packet()
#         print " created packet"
#         print "printing all the keys",keys
#         for k in keys:
#             print "k=",k
#             p.get(k, key=k)
            
#         ans = yield p.send()
#         print "ans=",ans
#         self.serialLinks = dict((k, ans[k]) for k in keys)


#         # yield self.reg.cd(['','Servers',serverNameAD5764_DCBOX,'links'])
#         # keys = yield self.reg.dir()[1]
#         # print("Keys found: %s"%str(keys))
#         # p=reg.packet()

#         # for k in keys:
#         #     p.get(k,key=k)

#         # ans = yield p.send()
#         # print("Packets sent. Response: %s"%str(ans))
#         # self.serialLinks = {k:ans[k] for k in keys}

#         #from labrad.wrappers import connectAsync
#         #cxn=yield connectAsync()
#         #reg=cxn.registry
#         #context = yield cxn.context()
#         #self.serialLinks = {}
#         #print('SERVERS:',self.client.servers.keys())
    
#     @inlineCallbacks
#     def findDevices(self):

#         # Make sure the registry has the proper directories
#         self.client.registry.cd([''])
#         if not ('Servers' in self.client.registry.dir()[0]):
#             print("\nError: registry does not contain 'Servers' folder. Please run the Serial Device Manager.\n")
#             return []
#         self.client.registry.cd(['','Servers'])
#         if not (serverNameAD5764_DCBOX in self.client.registry.dir()[0]):
#             print("\nError: registry does not have any information about AD5764_DCBOX devices. Please make sure they are connected, and then run the Serial Device Manager.\n")
#             return []

#         self.client.registry.cd(['','Servers',serverNameAD5764_DCBOX])             # go to server directory
#         keys          = self.client.registry.dir()[1]                              # get list of keys
#         devices       = [self.client.registry.get(key) for key in keys]            # fetch each entry from its key
#         activePorts   = self.client[serial_server_name].list_serial_ports          # get list of active serial ports
#         activeDevices = [device for device in devices if device[1] in activePorts] # get list of devices whose ports are currently active

#         devs = []
#         self.voltages = []
#         for port in activePorts:
#             devs.append(('dcbox (%s)'%port,(self.client[serial_server_name],port)))
#             self.voltages.append([port]+['unknown' for pos in range(8)])
#         returnValue(devs)



#         # server  = self.client[serial_server_name]
#         # manager = self.client.serial_device_manager
#         # ports = yield manager.list_ad5764_dcbox_devices()

#         # devs = []
#         # self.voltages = []
#         # for port in ports:
#         #     devs.append(('dcbox (%s)'%port[0],(server,port[0])))
#         #     self.voltages.append([port[0]]+['unknown' for pos in range(8)])
#         # returnValue(devs)

    
#     @setting(100)
#     def connect(self,c,server,port):
#         dev=self.selectedDevice(c)
#         yield dev.connect(server,port)

#     @setting(200,port='i',voltage='v',returns='s')
#     def set_voltage(self,c,port,voltage):
#         #print(dir(c))
#         if not (port in range(8)):
#             returnValue("Error: invalid port number.")
#             return
#         if (voltage > 10) or (voltage < -10):
#             returnValue("Error: invalid voltage. It must be between -10 and 10.")
#             return
#         dev=self.selectedDevice(c)
#         ans=yield dev.set_voltage(port,voltage)

#         # port+1 since the first entry is the COM number
#         self.voltages[c['device']][port+1] = ans.partition(' TO ')[2][:-1]
#         returnValue(ans)

#     @setting(8998)
#     def read_voltages(self,c):
#         dev=self.selectedDevice(c)
#         for port in range(8):
#             yield dev.write("GET_DAC,%i\r"%port)
#             ans = yield dev.read()
#             self.voltages[c['device']][port+1] = ans
#         returnValue("DONE")

#     @setting(8999)
#     def get_voltages(self,c):
#         ret = yield self.voltages
#         returnValue(ret)
        
#     @setting(9001,v='v')
#     def do_nothing(self,c,v):
#         pass
#     @setting(9002)
#     def read(self,c):
#         dev=self.selectedDevice(c)
#         ret=yield dev.read()
#         returnValue(ret)
#     @setting(9003)
#     def write(self,c,phrase):
#         dev=self.selectedDevice(c)
#         yield dev.write(phrase)
#     @setting(9004)
#     def query(self,c,phrase):
#         dev=self.selectedDevice(c)
#         yield dev.write(phrase)
#         ret = yield dev.read()
#         returnValue(ret)

    
# __server__ = AD5764DcboxServer()

# if __name__ == '__main__':
#     from labrad import util
#     util.runServer(__server__)













