machinelearning

My first approach of machine learning

It is very helpful to know some python and machine learning basics to understand this.

So I think the best way of explaining what this all does is go to main.py line by line:

1-3: 
This should be clear to everyone:
math is used for the sigmoid function; and time for little delays

3-4: 
Here Im defining some arrays:
neurons isnt used at the moment so you can ignore this one.
Log is an array, where some steps are documented, you can print these to get a more detailed view of what it is doing there.

6-7: 
This is only a sigmoid you may be familiar with this, it gives you a value between 0 and 1 no matter what input you are giving to it, its used to make the nn non-linear.

9-17:
This is the Input Neuron class:
It has the init funcion where it (called at creation) gets its input value.
Also it defines an array where later the Synaps to forward data to are saved in.
The set_synaps function is for giving the Neuron ist Synaps to output data, since this gets called multiple times, it only appends the synaps and doesn't set the variable.
The go function gets called when the Neural Net is started. It only forward its input value to each of the Synaps in the Synaps array.

19-38:
This is the Hidden_layer_Neuron class:
In the Constructor it only creates two arrays; one for the Values it will get, one for the output Synaps, like in the Input Neuron class.
The set_ouput is the same as the set_synpas function in the Input Neuron class.
The get_output is only if you want later know where the Neuron is giving its Output to: It just returns the Synaps array.
The append_vls function is for giving the Neuron its input Values, since it will get multiple Inputs it appends it to the value array.
The run function is called when the nn is running; it sums up all the input it got, send it to the sigmoid function and gives it to each of the Synaps.
And here it apends something to the log array, you dont need to know what this is, and you cant either since its german.

40-51:
This is the OutputNeuron class:
In the constructor it defines a variable and an array which we will see later again.
The append_vls function gets a value appends it to the vls array and appends something to the log.
The get_output function only sums up all the inputs and returns them.

53-63:
This is the Synaps class:
it only has som Functions which I think are self explaining:
It gets a value multiplies it with a weight and gives it to the next neuron.

65-126:
This is the creator of the Neural Net:
First it sets some variables which become important later.
Then it creates one Input Neuron for each value in the Inputs array, which is an argument of the function.
After that it will create the Hidden Layers with the Hidden Neurons.
If there are more than one Hidden Layer it will create the Synaps between them.
Then it will create and set the Synaps between the Input Layer and the first Hidden Layer.


