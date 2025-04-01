import threading
import queue
import time
import random

class Stabilimento:

  def __init__(self):
    self.tipologia = ["Utilitaria", "Suv", "Sportiva"]
    self.fasi = ["Stampaggio", "Assemblaggio", "Verniciatura", "Montaggio", "Collaudo"]
    self.code = {tipo: [queue.Queue() for _ in range(len(self.fasi))] for tipo in self.tipologia}
    self.parametri = {"tempi": {}}

  # generazione casuale dei tempi di lavorazione per ogni tipologia/fase
  def genera_parametri(self, range_tempo):
    for tipo in self.tipologia:
      t = [0,0,0,0,0]
      for fase_index in range(len(self.fasi)):
        t[fase_index] = random.randint(range_tempo[0], range_tempo[1])
      self.parametri["tempi"][tipo] = t
    print("Generazione parametri completata.")

  # generazione casuale di ordini, inseriti nella coda della prima fase
  def genera_ordini(self, range_ordini):
    for tipo in self.tipologia:
      numero_ordini = random.randint(range_ordini[0], range_ordini[1])
      for _ in range(numero_ordini):
        self.code[tipo][0].put(tipo)
    print("Generazione ordini completata.")

  # esecuzione di una fase generica di produzione
  def lavorazione_fase(self, tipo, fase_index):
    while True:
      automobile = self.code[tipo][fase_index].get()
      tempo = self.parametri["tempi"][tipo][fase_index]
      print(f"{automobile}: fase {self.fasi[fase_index]} in corso ({tempo}s)...")
      time.sleep(tempo)
      print(f"{automobile}: fase {self.fasi[fase_index]} completata.")
      if fase_index < (len(self.fasi) - 1):
        self.code[tipo][fase_index + 1].put(automobile)
      self.code[tipo][fase_index].task_done()

  # avvio della produzione del lotto di ordini
  def avvio_produzione(self, range_ordini, range_tempo):
    start_time = time.time()
    self.genera_parametri(range_tempo)
    self.genera_ordini(range_ordini)
    for tipo in self.tipologia:
      for fase_index in range(len(self.fasi)):
        t = threading.Thread(target = self.lavorazione_fase, args = (tipo, fase_index))
        t.start()
    for tipo in self.tipologia:
      for fase_index in range(len(self.fasi)):
        self.code[tipo][fase_index].join()
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Produzione lotto completata in {total_time:.2f} secondi.")
