<!DOCTYPE html><html lang="zh-CN">
<html xmlns="http://www.w3.org/1999/xhtml">	
<body>
<h1>LCD2USB树莓派监控</h1>
<h2>===硬件===</h2>
<h3>需要有2个按钮[用于翻页]的LCD2USB的板子,上面接着2004的LCD,树莓派GPIO4上接温度计数据</h3>
<div>连接树莓派</div>
<table><tr>
<td><img src="https://github.com/MOEYUUKO/Rpi_USB2LCD/blob/master/image/1.jpg" height="200px"></td>
<td><img src="https://github.com/MOEYUUKO/Rpi_USB2LCD/blob/master/image/2.jpg" height="200px"></td>
</tr></table>
<div>目前的3页 往上一页然后长按可重启程序</div>
<table><tr>
<td><img src="https://github.com/MOEYUUKO/Rpi_USB2LCD/blob/master/image/3.jpg" height="200px"></td>
<td><img src="https://github.com/MOEYUUKO/Rpi_USB2LCD/blob/master/image/4.jpg" height="200px"></td>
<td><img src="https://github.com/MOEYUUKO/Rpi_USB2LCD/blob/master/image/5.jpg" height="200px"></td>
</tr></table>
<div>温度计连接</div>
<table><tr>
<td><img src="https://github.com/MOEYUUKO/Rpi_USB2LCD/blob/master/image/6.jpg" height="200px"></td>
<td><img src="https://github.com/MOEYUUKO/Rpi_USB2LCD/blob/master/image/7.jpg" height="200px"></td>
</tr></table>
<div>新加的气压传感器和光线传感器</div>
<table><tr>
<td><img src="https://github.com/MOEYUUKO/Rpi_USB2LCD/blob/master/image/8.jpg" height="100px"></td>
<td><img src="https://github.com/MOEYUUKO/Rpi_USB2LCD/blob/master/image/9.jpg" height="100px"></td>
<td><img src="https://github.com/MOEYUUKO/Rpi_USB2LCD/blob/master/image/10.jpg" height="100px"></td>
</tr></table>
<br>
<h2>===使用的开源项目===</h2>
<div>
<h3>LCD2USB库:</h3>
&nbsp;&nbsp;&nbsp;&nbsp;https://github.com/xyb/lcd2usb<br>
<br>
<h2>===依赖===</h2>
<h3>DHT22温度计库:</h3>
&nbsp;&nbsp;&nbsp;&nbsp; sudo git clone https://github.com/adafruit/Adafruit_Python_DHT.git<br>
&nbsp;&nbsp;&nbsp;&nbsp; cd Adafruit_Python_DHT/<br>
&nbsp;&nbsp;&nbsp;&nbsp; sudo python2.7 setup.py install<br>
<br>
<h3>ifstat网速监控(暂时使用):</h3>
&nbsp;&nbsp;&nbsp;&nbsp; sudo apt-get install ifstat
</div>
</body>
</html>