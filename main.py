import random
import matplotlib.pyplot as plt
import time
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import plotly.express as px

heatmap_size = 100 #Heat map width and height value
temp_var = []
okok = 0
for i in range(heatmap_size): #CREATES A LIST FOR X AND Y AXIS OF THE GRAPH
   temp_var.append(okok)
   okok = okok + 0.01 #modify to include heatmap variable ////////////////////

def model(N, T, L, s, ccc, mutation, costProducerFict, costProducerDoc, costConsumerFict, costConsumerDoc, gainProducerFict, gainProducerDoc, gainConsumerFict, gainConsumerDoc):
    
    temp_graphdata = [] #Temp variable used to store future graph data
    memory = [] #Stores a bunch of data /// NOT COMPLETE
    duration = 0 #Simulation length tracker
    initial_time = time.time() #Stores the time when the simulation starts
    
    probProducer = [] #probability for the producer to chose to produce a documentary
    probConsumer = [] #probability for the consumer to chose to consume a documentary

    for i in range(N): #generates the initial probabilities producers have to pick documentaries
        probProducer.append(random.random())

    for i in range(N): #generates the initial probabilities consumers have to pick documentaries
        probConsumer.append(random.random())

    memory.append(probConsumer)
    memory.append(probProducer)

    for i in range(T): #Main Loop
    
        producerChoice = [] #What the producers produce (in the format of a list)
        consumerChoice = [] 

        producerGains = [] #List containing the gains of each producer
        consumerGains = [] #List containing the gains of each consumer
    
        if i == 1: #We calculate how long it will take to run the simulation based on the number of generations and the time it took to run GEN1
            duration = int((end_time - start_time)*T)
        start_time = time.time()

        progress = int((i/T) * 100) + 1 #Progress bar to show how close we are done to finishing the simulation
        #print(f"Estimated total lenght: {duration} seconds | Task progress: {progress}%", end = '\r')
    
        for i in range(N):
            if random.random() <= probProducer[i]:
                producerChoice.append('D')
            else: 
                producerChoice.append('F')
            #Creates a list of type of works produced by the producer (F for fiction and D for documentary)

        indices_producer_f = [i for i, x in enumerate(producerChoice) if x == "F"] #grab the indice value of each fiction
        indices_producer_d = [i for i, x in enumerate(producerChoice) if x == "D"] #grab the indice value of each documentary

        consumerSelection = []
    
        for i in range(N * ccc):
            if len(indices_producer_f) == 0:
                consumerChoice.append('D')
                temp_choice = random.choice(indices_producer_d)
            elif len(indices_producer_d) == 0:
                consumerChoice.append('F')
                temp_choice = random.choice(indices_producer_f)
            else:
                if random.random() <= probConsumer[int(i/ccc)]:
                    temp_choice = random.choice(indices_producer_d)
                    consumerChoice.append('D')
                else:
                    temp_choice = random.choice(indices_producer_f)
                    consumerChoice.append('F')

            consumerSelection.append(temp_choice)
            #creates a list of indices picked by consumers. These indices link back to the original list of  ['D', 'F', 'D'].
            #also creates a list of what consumers have picked, so we can calculate their costs and gains

        appearances = []
        for i in range(N): #Creates a list of the frequency each indice (linked to a producer) appears
            appearances.append(consumerSelection.count(i))
    
        for i in range(N): #Using the frequency each producer is picked, we can calculate their gain by linking them back to which item they originally produced
            if producerChoice[i] == 'D':
                producerGains.append((appearances[i] * gainProducerDoc) - costProducerDoc)
            else:
                producerGains.append((appearances[i] * gainProducerFict) - costProducerFict)
    
        consumer_d = 0
        consumer_f = 0
        for i in range(N*ccc): #Same thing than above, but checking for documentary producers
            if consumerChoice[i] == 'D':
                consumer_d = consumer_d + 1
            else:
                consumer_f = consumer_f + 1
            if consumer_d + consumer_f == ccc:
                gainConsumer = (1 - L) * ((consumer_d*gainConsumerDoc) + (consumer_f*gainConsumerFict)) +(L * consumer_d * consumer_f) - (costConsumerFict * consumer_f) - (costConsumerDoc * consumer_d)
                consumerGains.append(gainConsumer)
                consumer_d = 0
                consumer_f = 0

        positive_preproducerGains = [x + abs(min(producerGains)) for x in producerGains]
        unified_preproducerGains = [x / sum(positive_preproducerGains) for x in positive_preproducerGains] #Makes it so the sum of producer gains is equal to 1
    
        producerGains = []
        for i in range(N):
            producerGains.append(1 - s * (1 - unified_preproducerGains[i]))

        unified_producerGains = [x / sum(producerGains) for x in producerGains]
        
        positive_consumerGains = [x + abs(min(consumerGains)) for x in consumerGains]
        if sum(positive_consumerGains) == 0: #CASE where consumer gain is 0, each consumer is given an equal probability of getting picked later on using this line
            positive_consumerGains = [x + 1 for x in positive_consumerGains]
        
        unified_consumerGains = [x / sum(positive_consumerGains) for x in positive_consumerGains] #Makes it so the sum of consumer gains is equal to 1

        unified_one_producerGains = []
        for i in range(N): #Adds the unified producer gains together so that the lists increases until it reaches one "(0.1, 0.4, 0.8, 1)"
            if len(unified_one_producerGains) == 0:
                l = 0
            else:
                l = unified_one_producerGains[i - 1]

            unified_one_producerGains.append(l + unified_producerGains[i])


        unified_one_consumerGains = []
        for i in range(N): #Adds the unified consumer gains together so that the lists increases until it reaches one "(0.1, 0.4, 0.8, 1)"
            if len(unified_one_consumerGains) == 0:
                l = 0
            else:
                l = unified_one_consumerGains[i - 1]

            unified_one_consumerGains.append(l + unified_consumerGains[i])
    
        new_prob_producer = []
        for i in range(N): #Copies previous producer strategies, with more chance of picking one that had higher gains
            counter_eight = 0
            temp_random = random.random()
        
            for i in range(N):
                if temp_random > unified_one_producerGains[counter_eight]:
                    counter_eight = counter_eight + 1

                else:
                    break
         
            new_prob_producer.append(probProducer[counter_eight])
    
        probProducer = new_prob_producer

        new_new_prob_producer = []
        for i in range(N): #Creates noise to slightly modify the simulation. The value of the noise can be modified at the start of the code
            k = random.random()
            if (k <= 0.25) and (probProducer[i] > mutation):
                new_new_prob_producer.append(probProducer[i] - mutation)
            elif (k >= 0.75) and (probProducer[i] < (1 - mutation)):
                new_new_prob_producer.append(probProducer[i] + mutation)
            else:
                new_new_prob_producer.append(probProducer[i])

        probProducer = new_new_prob_producer

        new_prob_consumer = []
        for i in range(N): #Copies previous consumer strategies, with more chance of picking one that had higher gains
            counter_nine = 0
            temp_random = random.random()

            for i in range(N):
                if temp_random > unified_one_consumerGains[counter_nine]:
                    counter_nine = counter_nine + 1
                else:
                    break
        
            new_prob_consumer.append(probConsumer[counter_nine])

        probConsumer = new_prob_consumer

        new_new_prob_consumer = []
        for i in range(N): #Creates noise to slightly modify the simulation
            k = random.random() 
            if (k <= 0.25) and (probConsumer[i] > mutation):
                new_new_prob_consumer.append(probConsumer[i] - mutation)
            elif (k >= 0.75) and (probConsumer[i] < (1 - mutation)):
                new_new_prob_consumer.append(probConsumer[i] + mutation)
            else:
                new_new_prob_consumer.append(probConsumer[i])
            
        probConsumer = new_new_prob_consumer

        temp_graphdata.append(sum(probProducer)/len(probProducer)) #Temporarily produces a graph
    
        memory.append(probConsumer)
        memory.append(probProducer)
        #Attempts for a single variable to store all of the useful data /// WORK IN PROGRESS

        end_time = time.time()
    
    final_time = time.time() #Stores the time at which the simulation finishes
    #print(f"Simulation complete, it took {int(final_time - initial_time)} seconds to complete the simulation!") #Prints total time for the simulation

    return(probProducer)

probProducer = []
graphdata = []
full_data = []

for i in range(heatmap_size):

    costConsumerFict = 0.01 + (i/100) 

    print(i)
    graphdata = []

    for i in range (heatmap_size):

        L = 0.00 #(i/100) #///////////////////// FUTURE GAIN FOR CONSUMERS FROM CONSUMING BOTH FICTION AND DOCUMENTARIES

        mutation = 0.01 #Generates noise

        s = 1 #influence that producer gains have on future generations

        ccc = 2 #Consumer Purchase Count --> How many fictions/documentaries each consumer buys

        costProducerFict = 0.01 + (i/100) #+ (i/100)
        costProducerDoc = 0.5 #How much it costs the producer to make a documentary

        #costConsumerFict = 0.5 #How much it costs the consumer to buy a film (fiction)
        costConsumerDoc = 0.5 #How much it costs the consumer to buy a documentary

        gainProducerFict = 0.5 #How much the producer gains from each sold film (fiction)
        gainProducerDoc = 0.5 #How much the producer gains from each sold documentary ERROR HERE IF VALUE TOO SMALL CHECK WHY

        gainConsumerFict = 0.5 #How much the consumer gains from watching a film (fiction)
        gainConsumerDoc = 0.5 #How much the consumer gains from watching a documentary

        N = 100 #Population size
        T = N #Number of generations

        gp = model(N, T, L, s, ccc, mutation, costProducerFict, costProducerDoc, costConsumerFict, costConsumerDoc, gainProducerFict, gainProducerDoc, gainConsumerFict, gainConsumerDoc)
        graphdata.append(1 - (sum(gp)/len(gp)))
 
    full_data.append(graphdata)
    
fig = px.imshow(full_data, text_auto=True, labels = {"x":"Fiction producer cost", "y":"Fiction Consumer Cost", "color":"Average probability to produce fiction"}, title = "Effects of Producer cost and Consumer cost on the production of fiction", x = temp_var, y = temp_var, origin='lower')

fig.show()
