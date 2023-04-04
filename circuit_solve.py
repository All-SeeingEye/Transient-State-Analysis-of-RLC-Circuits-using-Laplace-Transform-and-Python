from parsing_circuit import *
import sympy as sp
import matplotlib.pyplot as plt
import sys
import subprocess


if len(sys.argv) != 3:
    print("Usage: python circuit_solve.py <input> <input>")
    sys.exit(1)

if sys.argv[2] == '.tran':

    netlist = sys.argv[1]
    data_un = parse_circuit(netlist)
    data,flag_ac,flag_dc,w0,mode = process_net(data_un)
    rlc_count,v_count,i_count,line_count = Error(data)
    data_dic = {'element':[],'+node':[],'-node':[],'value':[],'phase':[]}
    load_data(data,data_dic,mode)
    num_nodes = count_nodes(len(data),data_dic)
    branch_count = len(data)
    #Start solving the circuit

    #make matricies for calculations
    #V matrix to store variable names of voltage nodes
    V = sp.zeros(num_nodes,1)
    #I matrix to store values of independent current sources
    # I = np.zeros((num_nodes,1),dtype='complex_')
    I =  sp.zeros(num_nodes,1)
    #G matrix as in conductance matrix for the equations
    G = np.zeros((num_nodes,num_nodes),dtype='complex_')
    GS = sp.zeros(num_nodes,num_nodes)
    s = sp.Symbol('s')

    # count the number of element types that affect the size of the B, C, D, E and J arrays
    k = v_count
    if k != 0:
        B = sp.zeros(num_nodes,k)
        C = sp.zeros(k,num_nodes)
        D = sp.zeros(k,k)
        E = sp.zeros(k,1)
        J = sp.zeros(k,1)

    gs = 0
    for i in range(branch_count):  
        n1 = data_dic['+node'][i] #first node is + 
        n2 = data_dic['-node'][i] #second node is - 
        # iterate through each element and save them in temporary variable g
        # then appy the rules to make G matrix
        comp = data_dic['element'][i][0]   #The first letter shows element type
        if comp == 'R':
            gs = 1/sp.sympify(data_dic['element'][i])
            g = 1/data_dic['value'][i] 
        if comp == 'L':
            gs = 1/(s*sp.sympify(data_dic['element'][i]))
            if mode == 'ac':
                g = 1/(1j*w0*data_dic['value'][i]) 
            else:
                g = np.inf                          #for dc L behaves as close circuit in steady state
        if comp == 'C':
            gs = s*sp.sympify(data_dic['element'][i])
            if mode == 'ac':
                g = 1j*w0*data_dic['value'][i]     
            else:
                g = 0                               #for dc C behaves as open circuit in steady state

        if (comp == 'R') or (comp == 'L') or (comp == 'C'):
            # If neither side of the element is connected to ground
            # then subtract it from appropriate location in matrix.
            if (n1 != 0) and (n2 != 0):
                G[n1-1,n2-1] += -g
                G[n2-1,n1-1] += -g
                
                GS[n1-1,n2-1] += -gs
                GS[n2-1,n1-1] += -gs

            # If node 1 is connected to ground, add element to diagonal of matrix
            if n1 != 0:
                G[n1-1,n1-1] += g
                GS[n1-1,n1-1] += gs

            # same for for node 2
            if n2 != 0:
                G[n2-1,n2-1] += g
                GS[n2-1,n2-1] += gs

    # generate the B Matrix
    # loop through all the branches and process independent voltage sources
    sources = 0   # count source number
    for i in range(branch_count):
        n1 = data_dic['+node'][i]
        n2 = data_dic['-node'][i]
        # process all the independent voltage sources
        #x = df.loc[i,'element'][0]   #get 1st letter of element name
        comp = data_dic['element'][i][0]
        if comp == 'V':
            if v_count > 1:
                if n1 != 0:
                    B[n1-1][sources] = 1
                if n2 != 0:
                    B[n2-1][sources] = -1
                sources += 1   #increment source count
            else:
                if n1 != 0:
                    B[n1-1] = -1
                if n2 != 0:
                    B[n2-1] = 1


    source = 0   # count source number
    for i in range(branch_count):
        #n1 = df.loc[i,'p node']
        n1 = data_dic['+node'][i]
        n2 = data_dic['-node'][i]
        # process all the independent voltage sources
        #x = df.loc[i,'element'][0]   #get 1st letter of element name
        comp = data_dic['element'][i][0]
        if comp == 'V':
            if v_count > 1:
                if n1 != 0:
                    C[source][n1-1] = 1
                if n2 != 0:
                    C[source][n2-1] = -1
                source += 1   #increment source count
            else:
                if n1 != 0:
                    C[n1-1] = -1
                if n2 != 0:
                    C[n2-1] = 1



    # Current matrix containg current at each node
    for i in range(branch_count):
        #n1 = df.loc[i,'p node']
        n1 = data_dic['+node'][i]
        n2 = data_dic['-node'][i]
        # process all the passive elements, save conductance to temp value
        comp = data_dic['element'][i][0]
        if comp == 'I':
            #g = data_dic['element'][i]
            g = data_dic['value'][i]*np.exp(1j*data_dic['phase'][i]) # For AC in, case dc phase = 0
            #g = data_dic['value'][i]
            # sum the current into each node
            if n1 != 0:
                I[n1-1] = I[n1-1] - g
            if n2 != 0:
                I[n2-1] = I[n2-1] + g


    for i in range(num_nodes):
        V[i] = sp.sympify('v{:d}'.format(i+1))


    # matrix J for current through voltage sources
    sources = 0   # count source number
    for i in range(branch_count):
        # process all the passive elements
        comp = data_dic['element'][i][0]  
        if comp == 'V':
            #J[sorces] = sympify('I_{:s}'.format(df.loc[i,'element']))
            J[sources] = 'I_{:s}'.format(data_dic['element'][i])
            sources += 1

    # generate the E matrix
    sn = 0   # count source number
    for i in range(branch_count):
        # process all the passive elements
        x = data_dic['element'][i][0]   #get 1st letter of element name
        if x == 'V':
            E[sn] = sp.sympify(data_dic['element'][i])
            sn += 1


    Z = sp.Matrix(I[:] + E[:])
    X = sp.Matrix(V[:] + J[:])

    n = num_nodes
    m = v_count
    A = sp.zeros(m+n,m+n)
    for i in range(n):
        for j in range(n):
            A[i,j] = GS[i,j]

    if v_count > 1:
        for i in range(n):
            for j in range(m):
                A[i,n+j] = B[i,j]
                A[n+j,i] = C[j,i]
    else:
        for i in range(n):
            A[i,n] = B[i]
            A[n,i] = C[i]

    solutions = sp.solve(A*X-Z,X)
    new_dict_un = dict(zip(data_dic["element"], data_dic["value"]))
    new_dict = {sp.symbols(key): value for key, value in new_dict_un.items()}

    print(list(X))
    what = input('Node/Branch: ')

    #-------------------------------------------------------
    sus = solutions[sp.Symbol(what)].subs(new_dict)
    #-------------------------------------------------------

    t = sp.Symbol('t')
    def invL(F):
        return sp.inverse_laplace_transform(F, s, t)

    k = invL(sus)
    kreal,kimag = k.as_real_imag()

    time = np.linspace(0,15,100)
    y = []
    for tt in time:
        y.append(kreal.subs({t:tt}))
    values= []
    times = []
    zipps = list(zip(y,time))
    for i,tt in zipps:
        try:
            values.append(float(i))
            times.append(float(tt))
        except:
            pass


    fig, ax = plt.subplots()
    ax.plot(times, values)
    ax.set_ylabel(what)
    ax.set_xlabel('Time')
    plt.show()

elif sys.argv[2] == '.draw':
    args = sys.argv[1:]
    subprocess.call(['python3', 'draw.py'] + args)
else:
    print("Usage: python circuit_solve.py <input> <trans/draw>")
    sys.exit(1)

