import threading
import queue
import time
import random

class Stabilimento:

  def __init__(self):
    self.tipologia = ["Utilitaria", "Suv", "Sportiva"]
    self.fasi = ["Stampaggio", "Assemblaggio", "Verniciatura", "Montaggio", "Collaudo"]
    self.code = {tipo: [queue.Queue() for _ in range(len(self.fasi))] for tipo in self.tipologia}
    self.parametri = {"tempi": {}, "prob_guasto": 0}

  # generazione dei parametri della simulazione
  def genera_parametri(self, range_tempo, prob_guasto):
    if ((range_tempo[0] < 0) or (range_tempo[1] < 0)):
      raise ValueError("Range tempi non valido.")
    if ((prob_guasto < 0) or (prob_guasto > 1)):
      raise ValueError("Il valore di probabilità deve essere compreso tra 0 e 1.")
    for tipo in self.tipologia:
      t = [0,0,0,0,0]
      for fase_index in range(len(self.fasi)):
        t[fase_index] = random.randint(range_tempo[0], range_tempo[1])
      self.parametri["tempi"][tipo] = t
    self.parametri["prob_guasto"] = prob_guasto
    print("Generazione parametri completata.")

  # generazione casuale di ordini, inseriti nella coda della prima fase
  def genera_ordini(self, range_ordini):
    if ((range_ordini[0] < 0) or (range_ordini[1] < 0)):
      raise ValueError("Range ordini non valido.")
    for tipo in self.tipologia:
      numero_ordini = random.randint(range_ordini[0], range_ordini[1])
      for i in range(numero_ordini):
        tipo_i = tipo + str(i)
        self.code[tipo][0].put(tipo_i)
    print("Generazione ordini completata.")

  # esecuzione di una fase generica di produzione
  def lavorazione_fase(self, tipo, fase_index, range_tempo):
    while True:
      guasto = random.choices([0, 1], weights = [1 - self.parametri["prob_guasto"], self.parametri["prob_guasto"]], k = 1)[0]
      automobile = self.code[tipo][fase_index].get()
      tempo = self.parametri["tempi"][tipo][fase_index]
      print(f"{automobile}: fase {self.fasi[fase_index]} in corso ({tempo}s)...")
      time.sleep(tempo)
      if (guasto == 1):
        tempo_guasto = random.randint(range_tempo[0], range_tempo[1])
        print(f"Si è verificato un guasto: la produzione riprenderà tra {tempo_guasto} secondi.")
        time.sleep(tempo_guasto)
      print(f"{automobile}: fase {self.fasi[fase_index]} completata.")
      if fase_index < (len(self.fasi) - 1):
        self.code[tipo][fase_index + 1].put(automobile)
      self.code[tipo][fase_index].task_done()

  # avvio della produzione del lotto di ordini
  def avvio_produzione(self, range_ordini, range_tempo, prob_guasto):
    start_time = time.time()
    self.genera_parametri(range_tempo, prob_guasto)
    self.genera_ordini(range_ordini)
    for tipo in self.tipologia:
      for fase_index in range(len(self.fasi)):
        t = threading.Thread(target = self.lavorazione_fase, args = (tipo, fase_index, range_tempo), daemon = True)
        t.start()
    for tipo in self.tipologia:
      for fase_index in range(len(self.fasi)):
        self.code[tipo][fase_index].join()
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Produzione lotto completata in {total_time:.2f} secondi.")
