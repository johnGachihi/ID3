def adjust_weights(learning_rate,inputs,expected_output,initial_weights):
    new_w=[]
    old_w=initial_weights
    
    predicted_output=final_outputs(inputs,expected_output,initial_weights)
    node_error=compute_error(expected_output,predicted_output)
    for t in range(0,len(node_error)):
        skew_w=learning_rate*node_error[t]*predicted_output[t]
        new_w.append(old_w[t]+skew_w)
    return new_w

def compute_error(expected_output,predicted_output):
    error_list=[]
    T,o_k=expected_output,predicted_output
    print(expected_output,predicted_output)
    for r in range(0,len(expected_output)):
        error=(T[r]-o_k[r])*(o_k[r]*(1-o_k[r]))
        error_list.append(error)
    print("Error List: ",error_list)
    return error_list

def threshold(summation):#step function
    if(summation>0):
        return 1
    else:
        return 0

def predicted_output(inputs,weights):
    #print(input_1,input_2)
    for t in range(0,len(inputs)-1):
        x_1,x_2=inputs[t],inputs[t+1]
        w_1,w_2=weights[t],weights[t+1]
        summation=(x_1*w_1)+(x_2*w_2)
        output=threshold(summation)
        #print(x_1,w_1,"||",x_2,w_2)
        return output 
    
def final_outputs(inputs,expected_output,weights):
    p_output=[]
    #print(len(inputs))
    for k in range(0,len(inputs)):
        #for t in range(0,len(inputs[0])):
            #predicted_output(inputs[k][t],inputs[k][t+1],weights[t])
        p_output.append(predicted_output(inputs[k],weights))
    return p_output

def final_weight_for_correct_output(inputs,expected_output,initial_weights):
    learning_rate=0.5
    final_weights=[]
    for t in range(0,len(inputs)):
        for k in range(len(inputs[0])):
            while inputs[k][t]!=expected_output[k]:#this is a very strict PAC the iteration might never stop
                final_weights=adjust_weights(learning_rate,inputs,expected_output,initial_weights)
    return final_weights

    
inputs=[[0,0],[0,1],[1,0],[1,1]]#boolean logic target xor gate
expected_output=[0,1,1,0]
initial_weights=[0.1,0.5,-0.5,0.2,0.1,0.5]
final_weights=final_weight_for_correct_output(inputs,expected_output,initial_weights)
print(final_weights)
