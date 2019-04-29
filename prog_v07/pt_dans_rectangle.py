def pt_dans_rectangle(Lpt,pttest):
    if(pttest[0]<=Lpt[1][0]):
       return(0)##indique que pas dans le rectangle
    if (pttest[0]<=Lpt[0][0]):
       return(0)
    if (pttest[1]<=Lpt[2][1]):
       return(0)
    if (pttest[1]>=Lpt[1][1]):
        return(0)
    return(1)
        
Lpt=[[1,1],[1,8],[4,1],[4,8]]
pt=[2,2]
a=pt_dans_rectangle(Lpt,pt)
print(a)
