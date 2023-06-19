class ExamException(Exception):
    pass

class CSVTimeSeriesFile():
    def __init__(self, name):
        
        # Setto la variabile nome del file sulla quale viene istanziata la classe
        self.name = name

        # Provo ad aprire il file e leggere una riga per verificarne l'esistenza e che sia leggibile
        self.can_read = True
        try:
            my_file = open(self.name, 'r')
            my_file.readline()
        except Exception as e: # se non si può leggere
            self.can_read = False
            print('Errore in apertura del file')

    def get_data(self):
        
        if not self.can_read:
            
            # Se ho settato can_read a False vuol dire che il file non poteva essere aperto o era illeggibile
            # allora alzo una ExamException
            raise ExamException('errore, file non aperto o illeggibile')
            
            # Esco dalla funzione tornando "niente".
            return None

        else:
            
            # Inizializzo una lista vuota per salvare tutti i dati
            time_series = []
    
            # riapro il file
            my_file = open(self.name, 'r')
            #leggo line per linea il file
            for line in my_file:
                # faccio lo split della ',' e pulisco il carattere di newline dall'ultimo elemento con la funzione strip():
                elements=line.strip().split(',')
                #se NON processo l'intestazione:
                if elements[0]!= 'date':     
                    date=elements[0]
                    passengers=elements[1]
                    time_series.append([date,passengers])
            #faccio il check della timestamp        
            data_precedente=0
            for line in time_series:
                date=line[0]
                date_elements = date.split('-')
                if int(data_precedente) > int(date_elements[0]):
                    raise ExamException('Gli anni non sono ordinati in senso crescente')
                else:
                    data_precedente=date_elements[0]
                    
                    
            #chiudo il file e ritorno la lista
            my_file.close()    
            
            if time_series == []:
                raise ExamException('errore, nessun valore aveva i requisiti per esser aggiunto alla lista data')    
            # Quando ho processato tutte le righe, e controllato i dati ritorno la lista
            
        
        return time_series  

# chiusura classe CSVTimeSeriesFile che ritorna la lista di liste
        
        
        

def compute_avg_monthly_difference(time_series,first_year,last_year):
    try:
        first_year=int(first_year)
        last_year=int(last_year)
    except:
        raise ExamException('Gli anni non sono nel formato corretto')
    #controllo che la time_series non sia vuota
    if time_series==[]:
        raise ExamException('La lista "time_series è vuota"')
    #creo una lista 'years' per verificare first e last year
    #se first year è maggiore di last year alzo un eccezione
    if first_year>last_year:
        raise ExamException('Il valore di first è maggiore del valore di last year')
    #se first year è uguale a last year alzo un eccezione
    if first_year==last_year:
        raise ExamException('Il valore di first year è uguale a quello di last year')
    
    years=[]
    for line in time_series:
        date=line[0]
        date_elements = date.split('-') 
        try:
            years.append(int(date_elements[0]))
        except:
            raise ExamException('nessun anno è stato aggiunto alla lista')
    #se first year o last year non è nella lista viene alzata un eccezione
    if first_year not in years or last_year not in years:
        raise ExamException('Gli anni da valutare non sono validi')
    #creo un dizionario per salvare i dati dei passeggeri anno per anno e mese per mese
    passeggeri_per_anno={}
    for line in time_series:
        date=line[0]
        passengers=line[1]
        date_elements = date.split('-')
        try:
            year = int(date_elements[0])
            month = int(date_elements[1])
        except:
            raise ExamException('Il valore di mesi e anni non è valido')
        #se l'anno è nel range tra first e last year...
        if year in range(first_year,last_year+1):
            #...e non è gia presente nel dizionario allora aggiungo una lista vuota di 12 spazi con valore iniziale 'None'
            if year not in passeggeri_per_anno:
                passeggeri_per_anno[year] = [None] * 12
            #per ogni anno aggiungo i valori dei passeggeri mese per mese
            passeggeri_per_anno[year][month - 1] = passengers
    #se dopo il ciclo il dizionario è vuoto, alzo un eccezione
    if passeggeri_per_anno=={}:
        raise ExamException('Non è stato aggiunto alcun elemento al dizionario')
    #creo una lista somme per salvare le differenze dei passeggeri mese per mese, anno per anno
    
    somme=[]
    som=0
    #per ogni mese...
    for i in range(0,12):
        #per ogni anno tra first e last year (inclusi)...
        #calcolo la differenza tra i passeggeri nello stesso mese per anni consecutivi
        for year in range(first_year,last_year):
            som = som + (int(passeggeri_per_anno[year+1][i]) - int(passeggeri_per_anno[year][i]))
        #poi aggiungo i valori ottenuti alla lista somme
        try:
            somme.append(som) 
        except:
                raise ExamException('impossibile aggiungere questo elemento a "somme"')
        #reimposto som a zero per ricominciare il nuovo ciclo
        som=0
    #creo una lista per salvare le medie 
    medie=[]
    #per ogni elemento della lista somma, divido il valore per il numero di anni presi in considerazione 
    for item in somme:
        x=(item/(int(last_year)-int(first_year)))
        try:
            medie.append(x)
        except:
            raise ExamException('impossibile aggiungere questo elemento a "medie"')
    #ritorno la lista medie contenente quanto richiesto
    return medie

#esempio di utilizzo
#time_series_file=CSVTimeSeriesFile(name='data.csv')
#time_series = time_series_file.get_data()
#y=compute_avg_monthly_difference(time_series,"1949","1960")
#print(y)