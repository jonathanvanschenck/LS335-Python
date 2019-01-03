import ls335,time

ls = ls335.LS335(comport="COM3")
k = ls.getTemp()
ls.getTemp(unit="C")
ls.setSP(k+20)
ls.setRange("High")
while ls.getTemp<k+20:
  time.sleep(0.5)
  print("Temp: {}K, Heater: {}%".format(ls.getTemp(),ls.getHeat()/100))
ls.off()
ls.close()
