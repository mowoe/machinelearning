import math
import random
import time
import psutil
neurons = []
log = []

def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))

class InputNeuron(object):
    def __init__(self, value):
        self.value = value
        self.synaps = []
    def set_synaps(self, synaps):
        self.synaps.append(synaps)
    def go(self):
        for syns in self.synaps:
            syns.go(self.value)

class Hidden_layer_Neuron(object):
    def __init__(self):
        self.vls = []
        self.synaps = []
    def get_value(self, vls):
        self.vls = vls
    def set_output(self, outp):
        self.synaps.append(outp)
    def get_output(self):
        return self.synaps
    def append_vls(self, vl):
        self.vls.append(vl)
    def run(self):
        global log
        self.vl = 0
        for x in self.vls:
            self.vl += x
        self.vl = sigmoid(self.vl)
        for sins in self.synaps:
            sins.go(self.vl)
        log.append(("ich",self,"habe Wert",self.vl,"Synapse",self.synaps,"gegeben"))
        return self.vl

class OutputNeuron(object):
    def __init__(self):
        self.gesvls = 0
        self.vls = []
    def append_vls(self, vl):
        global log
        self.vls.append(vl)
        log.append(("mir wurde der Wert", vl, "appendet", self))
    def set_value(self, inp):
        self.inp = inp
    def get_output(self):
        for vl in self.vls:
            self.gesvls += vl
        return self.gesvls

class Synapse(object):
    def set_weight(self, weight):
        self.weight = weight
    def set_otput(self, out):
        self.outputob = out
    def get_weight(self):
        return self.weight
    def go(self, inputvl):
        self.inputvl = inputvl
        self.output = self.inputvl * self.weight
        self.outputob.append_vls(self.output)

def create_nn(values, no_hls, no_outputs, no_hneus, weights):
    global log
    ins = []
    hls = []
    syns = []
    outs = []
    i = 0
    while i < len(values):
        ins.append(InputNeuron(values[i]))
        i += 1
    for y in xrange(no_hls):
        hn = []
        for i in xrange(no_hneus):
            hn.append(Hidden_layer_Neuron())
        hls.append(hn)
    if len(hls) > 1:
        log.append(("detected multilayer", len(hls)))
        r = 0
        while r < len(hls[:-1]):
            for neurons in hls[r]:
                for neuron in hls[r+1]:
                    s = Synapse()
                    syns.append(s)
                    neurons.set_output(s)
                    s.set_otput(neuron)
                    log.append(("created Synapse",s,"taking Data from", neurons, "in Hidden Layer", r, "to Neuron", neuron, "in Hidden Layer", r+1))
            r+=1
    for input_neuron in ins:
        outs = []
        for hlns in hls[0]:
            syn = Synapse()
            syn.set_otput(hlns)
            log.append(("synapse wird Wert von",input_neuron,"an folgend weitergeben", hlns))
            syns.append(syn)
            input_neuron.set_synaps(syn)
    for i in  xrange(no_outputs):
        outs.append(OutputNeuron())
    log.append(outs)
    for hlns in hls[-1]:
        for out in outs:
            s = Synapse()
            hlns.set_output(s)
            s.set_otput(out)
            syns.append(s)
            log.append(("syapse", s, "wird ihren input an folgendes Output Neuron weitergeben", out))
    f = 0
    for hin in hn:
        log.append((hin.get_output(), "hierhin wird das hiddenlayer neuron ihren output geben"))
    while f <  len(syns):
        h = random.uniform(0, 50)
        syns[f].set_weight(weights[f])
        log.append(("ich habe der Synapse", syns[f], "den Wert", h, "zugewiesen!"))
        f +=1
    for input_neuron in ins:
        input_neuron.go()
    for hiddenlayer in hls:
        for hiddenneuron in hiddenlayer:
            log.append(("go", hiddenneuron, "in hidden Layer", hiddenlayer))
            hiddenneuron.run()
    outputs = []
    for out in outs:
        outputs.append(out.get_output())
    return outputs

def checkworks(oututs, des_outps, t=True):
    fc = 0
    oe = 0
    gerror = 0
    if len(oututs) != len(des_outps):
        print "not same lengths"
        exit()
    while oe < len(oututs):
        if oututs[oe] == des_outps[oe]:
            i = 0
        else:
            gerror += (oututs[oe] - des_outps[oe])
            fc += 1
        oe+=1
    if t == True:
        return gerror ** 2
    elif t == False:
        if fc == 0:
            print "feddig"
            return True
        else:
            return False

def train(inputs, no_outputs, des_outp):
    no_hneus = 1
    no_hls = 1
    no_weights = len(inputs) * no_hneus +  no_hneus * no_outputs
    if no_hneus > 1: no_weights += (no_hneus ** 2) * no_hls
    weights = []
    for x in xrange(no_weights):
        weights.append(1)
    schrittweite = 1
    print des_outp
    while create_nn(inputs, no_hls, no_outputs, no_hneus, weights) != des_outp:
        errora = checkworks(create_nn(inputs, no_hls, no_outputs, no_hneus, weights), des_outp)
        for j in xrange(len(weights)):
            weights[j] += schrittweite
            error = checkworks(create_nn(inputs, no_hls, no_outputs, no_hneus, weights), des_outp)
            if errora <= error:
                weights[j] -= schrittweite
                error = checkworks(create_nn(inputs, no_hls, no_outputs, no_hneus, weights), des_outp)
        for j in xrange(len(weights)):
            weights[j] -= schrittweite
            error = checkworks(create_nn(inputs, no_hls, no_outputs, no_hneus, weights), des_outp)
            if errora <= error:
                weights[j] += schrittweite
                error = checkworks(create_nn(inputs, no_hls, no_outputs, no_hneus, weights), des_outp)
        #print error, schrittweite, weights
        if errora == error:
            schrittweite = schrittweite / 2.0
        error = checkworks(create_nn(inputs, no_hls, no_outputs, no_hneus, weights), des_outp)
        outp = create_nn(inputs, no_hls, no_outputs, no_hneus, weights)
        if schrittweite == 0:
            no_hneus += 1
            if no_hneus == 10:
                no_hneus = 1
                no_hls += 1
            schrittweite = 1
            weights = []
            no_weights = len(inputs) * no_hneus + no_hneus * no_outputs
            if no_hneus > 1: no_weights += (no_hneus ** 2) * no_hls
            for x in xrange(no_weights):
                weights.append(1)
            print "halo i bims", no_hls, schrittweite, weights
        print "currently trying with",no_hls,"hidden layer with",no_hneus,"neuron each, with an error of", error, "i want output:", des_outp, "with a step of", schrittweite, "RAM Usage:", psutil.virtual_memory()[2], "%"
        time.sleep(0.01)
    print "ok finished learning process"
    print "ingredients:", (inputs, no_hls, no_outputs, no_hneus, weights)


train([300.29, 500.75], 1, [500.29])
