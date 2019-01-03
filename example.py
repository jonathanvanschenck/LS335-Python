import ls335,time

ls = ls335.LS335(comport="COM3")
k = ls.getTemp()
ls.getTemp(unit="C")
ls.setSP(k+5)
ls.setRange("High")
while ls.getTemp<k+5:
  time.sleep(0.5)
  print("Temp: {0:.2f}K, Heater: {0:.1f}%".format(ls.getTemp(),ls.getHeat()/100))
ls.off()
ls.close()
